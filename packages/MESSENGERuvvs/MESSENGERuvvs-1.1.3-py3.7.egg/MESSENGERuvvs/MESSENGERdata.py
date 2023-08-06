"""MESSENGER UVVS data class
Convert MESSENGER data into a useable class
*_temp.pickle are straight pickled versions of the IDL summmary files
Creates files that match my previous IDL summary files
This needs to be rerun if more methods are added to the class"""
import numpy as np
import os
import glob
import pickle
import pandas as pd
import bokeh.plotting as plt
from bokeh.models import HoverTool
from bokeh.palettes import Set1
from scipy import io
from astropy.time import Time
from astropy import units as u
from astropy.visualization import PercentileInterval
from solarsystemMB import SSObject, planet_geometry
from .database_setup import database_connect


def merc_year(datatime=None, initialize=False):
    """Insert/read start date for each Mercury year from database."""
    tstart = Time('2011-03-18T00:00:00', format='isot', scale='utc')
    tend = Time('2015-04-30T23:59:59', format='isot', scale='utc')

    if initialize:
        times_ = np.arange(tstart.jd, tend.jd)
        times = [Time(t, format='jd', scale='utc') for t in times_]

        taa = np.ndarray((len(times),))*u.rad
        for i,t in enumerate(times):
            time = Time(t, format='jd', scale='utc')
            geo = planet_geometry(time, 'Mercury')
            taa[i] = geo['taa']

        styear = [times[0]]
        for a,b,c in zip(taa[0:-1], taa[1:], times[1:]):
            if a > b:
                styear.append(c)
                print(c.iso)
        endyr = [*styear[1:], tend]

        with database_connect() as con:
            cur = con.cursor()
            try:
                cur.execute('DROP table MESmercyear')
            except:
                pass
            cur.execute('''CREATE table MESmercyear
                            (yrnum int PRIMARY KEY,
                             yrstart timestamp,
                             yrend timestamp)''')
            for i,d in enumerate(zip(styear, endyr)):
                cur.execute(f'''INSERT into MESmercyear
                                values ({i}, '{d[0].iso}', '{d[1].iso}')''')
    else:
        pass

    if datatime is not None:
        with database_connect() as con:
            yrnum = pd.read_sql('''SELECT * from MESmercyear''', con)

        myear = np.ndarray((len(datatime),), dtype=int)
        for i,yr in yrnum.iterrows():
            q = (datatime > yr.yrstart) & (datatime < yr.yrend)
            myear[q] = yr.yrnum

        return myear
    else:
        return None


class MESSENGERdata:
    def __init__(self, species=None, comparisons=None):
        """Retrieve MESSENGER data from database

        Species is required because each species is in different tables
        At least one SQL-formatted comparison is required."""
        allspecies = ['Na', 'Ca', 'Mg']
        if species is None:
            # Return an empty object
            self.species = None
            self.frame = None
            self.query = None
            self.data = None
            self.taa = None
        elif species not in allspecies:
            # Return list of valid species
            print(f"Valid species are {', '.join(allspecies)}")
            # Return an empty object
            self.species = None
            self.frame = None
            self.query = None
            self.data = None
            self.taa = None
        elif comparisons is None:
            # Return list of queryable fields
            with database_connect() as con:
                columns = pd.read_sql(
                    f'''SELECT * from {species}uvvsdata, {species}pointing
                        WHERE 1=2''', con)
            print('Available fields are:')
            for col in columns.columns:
                print(f'\t{col}')
            # Return an empty object
            self.species = None
            self.frame = None
            self.query = None
            self.data = None
            self.taa = None
        else:
            # Run the query and try to make the object
            query = f'''SELECT * from {species}uvvsdata, {species}pointing
                        WHERE unum=pnum and {comparisons}
                        ORDER BY unum'''
            try:
                with database_connect() as con:
                    data = pd.read_sql(query, con)
            except:
                print(query)
                assert 0, 'Problem with comparisons given.'

            if len(data) > 0:
                self.species = species
                self.frame = data.frame[0]
                self.query = comparisons
                data.drop(['species', 'frame'], inplace=True, axis=1)
                self.data = data
                self.data.set_index('unum', inplace=True)
                self.taa = np.median(data.taa)
            else:
                print(query)
                print('No data found')
                self.species = species
                self.query = comparisons
                self.frame = None
                self.data = None
                self.taa = None

    @staticmethod
    def initialize(datapath, database='thesolarsystemmb'):
        """Convert raw IDL sav files to pickles"""
        mercury = SSObject('Mercury')

        # Add to the database
        con = database_connect()
        cur = con.cursor()
        try:
            cur.execute('DROP table nauvvsdata')
            cur.execute('DROP table napointing')
            cur.execute('DROP table cauvvsdata')
            cur.execute('DROP table capointing')
            cur.execute('DROP table mguvvsdata')
            cur.execute('DROP table mgpointing')
        except:
            pass

        print('creating UVVS tables')
        spec = ['Ca', 'Na', 'Mg']
        for sp in spec:
            # Table with spectrum information
            cur.execute(f'''CREATE table {sp}uvvsdata (
                               unum SERIAL PRIMARY KEY,
                               species text,
                               frame text,
                               UTC timestamp,
                               orbit int,
                               merc_year int,
                               taa float,
                               rmerc float,
                               drdt float,
                               subslong float,
                               g float,
                               radiance float,
                               sigma float)''')

            # Table with MESSENGER geometry and UVVS pointing
            cur.execute(f'''CREATE table {sp}pointing (
                               pnum SERIAL PRIMARY KEY,
                               x float,
                               y float,
                               z float,
                               xbore float,
                               ybore float,
                               zbore float,
                               obstype text,
                               obstype_num int,
                               xtan float,
                               ytan float,
                               ztan float,
                               rtan float,
                               alttan float,
                               longtan float,
                               lattan float,
                               loctimetan float,
                               slit text)''')
            # Not including slit corners right now

        savfiles = glob.glob(datapath+'/*.sav')
        savfiles = sorted(savfiles)
        for oldfile in savfiles:
            # realfile = oldfile.replace('.sav', '_temp.pkl')
            newfile = oldfile.replace('.sav', '.pkl')
            print('{}\n{}\n***'.format(oldfile, newfile))
            data = io.readsav(oldfile, python_dict=True)
            # data = pickle.load(open(realfile, 'rb'))

            kR = u.def_unit('kR', 1e3*u.R)
            Rmerc = u.def_unit('R_Mercury', mercury.radius)
            nm = u.def_unit('nm', 1e-9*u.m)

            npts = len(data['orb_num'])
            species = os.path.basename(oldfile)[0:2].lower()

            # Determine UT for each spectrum
            t_iso = ['{}:{}:{}'.format('20' + time[0:2].decode('utf-8'),
                                       time[2:5].decode('utf-8'),
                                       time[6:].decode('utf-8'))
                     for time in data['step_utc_time']]
            UTC = Time(t_iso, format='yday')

            # Orbit number for each data spectrum
            orbit = np.array([int(o) for o in data['orb_num']])

            # determine Mercury year
            myear = merc_year(UTC)
            rmerc = (np.sqrt(np.sum(data['planet_sun_vector_tg']**2, axis=1)) *
                     u.km).to(u.AU)

            radiance = data[f'{species.lower()}_tot_rad_kr']
            sigma = radiance/data[f'{species.lower()}_tot_rad_snr']

            # Spacecraft position and boresight in MSO
            xyz = np.ndarray((npts, 3))
            bore = np.ndarray((npts, 3))
            corn0 = np.ndarray((npts, 3))
            corn1 = np.ndarray((npts, 3))
            corn2 = np.ndarray((npts, 3))
            corn3 = np.ndarray((npts, 3))
            for i in np.arange(npts):
                xyz[i,:] = np.dot(data['mso_rotation_matrix'][i,:,:],
                                  data['planet_sc_vector_tg'][i,:])/mercury.radius.value
                bore[i,:] = np.dot(data['mso_rotation_matrix'][i,:,:],
                                 data['boresight_unit_vector_center_tg'][i,:])
                corn0[i,:] = np.dot(data['mso_rotation_matrix'][i,:,:],
                                    data['boresight_unit_vector_c1_tg'][i,:])
                corn1[i,:] = np.dot(data['mso_rotation_matrix'][i,:,:],
                                    data['boresight_unit_vector_c2_tg'][i,:])
                corn2[i,:] = np.dot(data['mso_rotation_matrix'][i,:,:],
                                    data['boresight_unit_vector_c3_tg'][i,:])
                corn3[i,:] = np.dot(data['mso_rotation_matrix'][i,:,:],
                                    data['boresight_unit_vector_c4_tg'][i,:])

            xcorner = np.array([corn0[:,0], corn1[:,0],
                                corn2[:,0], corn3[:,0]]).transpose()
            ycorner = np.array([corn0[:,1], corn1[:,1],
                                corn2[:,1], corn3[:,1]]).transpose()
            zcorner = np.array([corn0[:,2], corn1[:,2],
                                corn2[:,2], corn3[:,2]]).transpose()

            # Determine tangent point
            rr = np.linalg.norm(xyz, axis=1)
            t = -np.sum(xyz*bore, axis=1)
            tanpt = xyz + bore*t[:,np.newaxis]
            rtan = np.linalg.norm(tanpt, axis=1)

            slit = np.array(['Surface' if s == 0 else 'Atmospheric'
                             for s in data['slit']])
            obstype = np.array([str(ob).replace('b', '').replace("'", '').strip()
                       for ob in data['obs_typ']])

            # Add in the spectra
            spectra = data[species.lower()+'_rad_kr']*kR
            wavelength = data['wavelength']*nm
            raw = data['orig']*u.ct
            try:
                corrected = data['fully_corr_cr']*u.ct
            except:
                corrected = data['corr']*u.ct
            dark = data['dark']*u.ct
            solarfit = data['sol_fit']*u.ct

            ndata = pd.DataFrame({
                        'species': species,
                        'frame': 'MSO',
                        'UTC': UTC,
                        'orbit': orbit,
                        'merc_year': myear,
                        'TAA': data['true_anomaly']*np.pi/180.,
                        'rmerc': rmerc.value,
                        'drdt': data['rad_vel'],
                        'subslong': data['subsolar_longitude']*np.pi/180.,
                        'g': data['gvals']/u.s,
                        'radiance': radiance,
                        'sigma': sigma,
                        'x': xyz[:,0] * Rmerc,
                        'y': xyz[:,1] * Rmerc,
                        'z': xyz[:,2] * Rmerc,
                        'xbore': bore[:,0],
                        'ybore': bore[:,1],
                        'zbore': bore[:,2],
                        'xcorn1': xcorner[:,0],
                        'xcorn2': xcorner[:,1],
                        'xcorn3': xcorner[:,2],
                        'xcorn4': xcorner[:,3],
                        'ycorn1': ycorner[:,0],
                        'ycorn2': ycorner[:,1],
                        'ycorn3': ycorner[:,2],
                        'ycorn4': ycorner[:,3],
                        'zcorn1': zcorner[:,0],
                        'zcorn2': zcorner[:,1],
                        'zcorn3': zcorner[:,2],
                        'zcorn4': zcorner[:,3],
                        'obstype': obstype,
                        'obstype_num': data['obs_typ_num'],
                        'xtan': tanpt[:,0],
                        'ytan': tanpt[:,1],
                        'ztan': tanpt[:,2],
                        'rtan': rtan,
                        'alttan': data['target_altitude_set'][:,0],
                        'minalt': data['minalt'],
                        'longtan': data['target_longitude_set'][:,0]*np.pi/180,
                        'lattan': data['target_latitude_set'][:,0]*np.pi/180,
                        'loctimetan': data['obs_solar_localtime'],
                        'slit': slit})
            ndata.fillna(-999, inplace=True)

            spectra = {'spectra': spectra,
                       'wavelength': wavelength,
                       'raw': raw,
                       'corrected': corrected,
                       'dark': dark,
                       'solarfit': solarfit}

            # save this for later
            with open(newfile, 'wb') as f:
                pickle.dump(ndata, f, pickle.HIGHEST_PROTOCOL)
            with open(newfile.replace('.pkl', '_spectra.pkl'), 'wb') as f:
                pickle.dump(spectra, f, pickle.HIGHEST_PROTOCOL)

            print('Inserting UVVS data')
            for i,dpoint in ndata.iterrows():
                cur.execute(f'''INSERT into {species}uvvsdata (
                                    species, frame, UTC, orbit, merc_year,
                                    taa, rmerc, drdt, subslong, g, radiance,
                                    sigma) values (
                                    '{dpoint.species}',
                                    '{dpoint.frame}',
                                    '{dpoint.UTC.iso}',
                                    {dpoint.orbit},
                                    {dpoint.merc_year},
                                    {dpoint.TAA},
                                    {dpoint.rmerc},
                                    {dpoint.drdt},
                                    {dpoint.subslong},
                                    {dpoint.g},
                                    {dpoint.radiance},
                                    {dpoint.sigma})''')
                cur.execute(f'''INSERT into {species}pointing (
                                    x, y, z, xbore, ybore, zbore,
                                    obstype, obstype_num, xtan, ytan, ztan,
                                    rtan, alttan, longtan, lattan,
                                    loctimetan, slit) values (
                                    {dpoint.x},
                                    {dpoint.y},
                                    {dpoint.z},
                                    {dpoint.xbore},
                                    {dpoint.ybore},
                                    {dpoint.zbore},
                                    '{dpoint.obstype}',
                                    {dpoint.obstype_num},
                                    {dpoint.xtan},
                                    {dpoint.ytan},
                                    {dpoint.ztan},
                                    {dpoint.rtan},
                                    {dpoint.alttan},
                                    {dpoint.longtan},
                                    {dpoint.lattan},
                                    {dpoint.loctimetan},
                                    '{dpoint.slit}')''')
        con.close()

    def __str__(self):
        result = (f'Species: {self.species}\n'
                  f'Query: {self.query}\n'
                  f'Frame: {self.frame}\n'
                  f'Object contains {len(self)} spectra.')
        return result

    def __repr__(self):
        result = ('MESSENGER UVVS Data Object\n'
                  f'Species: {self.species}\n'
                  f'Query: {self.query}\n'
                  f'Frame: {self.frame}\n'
                  f'Object contains {len(self)} spectra.')
        return result

    def __len__(self):
        try:
            return len(self.data)
        except:
            return 0

    def __getitem__(self, q_):
        if isinstance(q_, int):
            q = slice(q_, q_+1)
        elif isinstance(q_, slice):
            q = q_
        else:
            raise TypeError

        new = MESSENGERdata()
        new.species = self.species
        new.frame = self.frame
        new.query = self.query
        new.taa = self.taa
        new.data = self.data.iloc[q].copy()
        try:
            new.modelstrength = self.modelstrength
        except:
            pass

        return new

    def __iter__(self):
        for i in range(len(self.data)):
            yield self[i]

    def keys(self):
        keys = list(self.__dict__.keys())
        keys.extend([f'data.{col}' for col in self.data.columns])
        return keys

    def set_frame(self, frame=None):
        """Convert between MSO and Model frames.

        More frames could be added if necessary.
        If Frame is not specified, flips between MSO and Model."""
        if (frame is None) and (self.frame == 'MSO'):
            frame = 'Model'
        elif (frame is None) and (self.frame == 'Model'):
            frame = 'MSO'
        else:
            pass

        allframes = ['Model', 'MSO']
        if frame not in allframes:
            print('{} is not a valid frame.'.format(frame))
            return None
        elif frame == self.frame:
            pass
        elif (self.frame == 'MSO') and (frame == 'Model'):
            # Convert from MSO to Model
            self.data.x, self.data.y = self.data.y.copy(), -self.data.x.copy()
            self.data.xbore, self.data.ybore = (self.data.ybore.copy(),
                                                -self.data.xbore.copy())
            # self.data.xcorner, self.data.ycorner = (self.data.ycorner,
            #                                         -self.data.xcorner)
            self.data.xtan, self.data.ytan = (self.data.ytan.copy(),
                                              -self.data.xtan.copy())
            self.frame = 'Model'
        elif (self.frame == 'Model') and (frame == 'MSO'):
            self.data.x, self.data.y = -self.data.y.copy(), self.data.x.copy()
            self.data.xbore, self.data.ybore = (-self.data.ybore.copy(),
                                                self.data.xbore.copy())
            # self.data.xcorner, self.data.ycorner = (-self.data.ycorner,
            #                                         self.data.xcorner)
            self.data.xtan, self.data.ytan = (-self.data.ytan.copy(),
                                              self.data.xtan.copy())
            self.frame = 'MSO'
        else:
            assert 0, 'You somehow picked a bad combination.'

    def model(self, inputs_, npackets, quantity='radiance',
              dphi=3*u.deg, overwrite=False, filenames=None, label=None):
        from nexoclom import Input, modeldriver, LOSResult

        if isinstance(inputs_, str):
            inputs = Input(inputs_)
        elif isinstance(inputs_, Input):
            inputs = inputs_

        # TAA needs to match the data
        oldtaa = inputs.geometry.taa
        if len(set(self.data.orbit.tolist())) == 1:
            inputs.geometry.taa = np.median(self.data.taa)*u.rad
        elif np.max(self.data.taa)-np.min(self.data.taa) < 3*np.pi/180.:
            inputs.geometry.taa = np.median(self.data.taa)*u.rad
        else:
            assert 0, 'Too wide a range of taa'

        # Run the model
        modeldriver(inputs, npackets, overwrite=overwrite)

        # Simulate the data
        if 'inputs' in self.keys():
            self.inputs.append(inputs)
        else:
            self.inputs = [inputs]

        self.set_frame('Model')
        modelresult = LOSResult(inputs, self.data, quantity,
                                dphi=dphi, filenames=filenames,
                                overwrite=overwrite)
        modkey = f'model{len(self.inputs)-1:00d}'
        self.data[modkey] = modelresult.radiance/1e3 # Convert to kR

        interval = PercentileInterval(50)
        lim = interval.get_limits(self.data.radiance)
        mask = ((self.data.radiance >= lim[0]) &
                (self.data.radiance <= lim[1]))

        strunit = u.def_unit('10**26 atoms/s', 1e26/u.s)
        m_data = np.mean(self.data.radiance[mask])
        m_model = np.mean(self.data[modkey][mask])
        modelstrength = m_data/m_model * strunit * strunit
        self.data[modkey] = self.data[modkey] * modelstrength.value

        if 'modelstrength' in self.keys():
            self.modelstrength.append(modelstrength)
        else:
            self.modelstrength = [modelstrength]

        if label is None:
            label = modkey
        else:
            pass
        if 'modellabel' in self.keys():
            self.modellabel.append(label)
        else:
            self.modellabel = [label]

        if 'modelkey' in self.keys():
            self.modelkey.append(modkey)
        else:
            self.modelkey = [modkey]

        print(f'Model strength for {label} = {modelstrength}')

        # Put the old TAA back in.
        inputs.geometry.taa = oldtaa

    def plot(self, filename=None, show=True, **kwargs):
        if filename is not None:
            if not filename.endswith('.html'):
                filename += '.html'
            else:
                pass
            plt.output_file(filename)
        else:
            pass

        # Format the date correction
        self.data['utcstr'] = self.data['utc'].apply(
            lambda x: x.isoformat()[0:19])

        # Put the dataframe in a useable form
        source = plt.ColumnDataSource(self.data)

        # Make the figure
        fig = plt.figure(plot_width=1200, plot_height=800,
                         x_axis_type='datetime',
                         title=f'{self.species}, {self.query}',
                         x_axis_label='UTC',
                         y_axis_label='Radiance (kR)',
                         tools=['pan', 'box_zoom', 'reset', 'save'])

        # plot the data
        dplot = fig.circle(x='utc', y='radiance', size=7, color='black',
                           legend='Data', hover_color='white', source=source)

        # tool tips
        tips = [('index', '$index'), ('UTC', '@utcstr'),
                ('Radiance', '@radiance{0.2f} kR')]
        for modkey, modlabel in zip(self.modelkey, self.modellabel):
            tips.append((modlabel, f'@{modkey}{{0.2f}} kR'))
        datahover = HoverTool(tooltips=tips,
                              renderers=[dplot])
        fig.add_tools(datahover)

        # Plot the model
        col = (c for c in Set1[9])
        for modkey,modlabel in zip(self.modelkey, self.modellabel):
            try:
                c = next(col)
            except StopIteration:
                col = (c for c in Set1[9])
                c = next(col)

            fig.line(self.data.utc, self.data[modkey], legend=modlabel)
            f = fig.circle(x='utc', y=modkey, size=7, source=source,
                           legend=modlabel, color=next(col))
            datahover.renderers.append(f)

        # Labels, etc.
        fig.title.align = 'center'
        fig.title.text_font_size = '16pt'
        fig.axis.axis_label_text_font_size = '16pt'
        fig.axis.major_label_text_font_size = '16pt'
        fig.legend.label_text_font_size = '16pt'
        fig.legend.click_policy = 'hide'

        if filename is not None:
            plt.output_file(filename)
            plt.save(fig)
        else:
            pass

        if show:
            plt.show(fig)

    def export(self, filename, columns=['utc', 'radiance']):
        columns_ = columns.copy()
        if 'modelkey' in self.keys():
            columns_.extend(self.modelkey)
        else: pass

        # Make sure radiance is in there
        if 'radiance' not in columns_:
            columns_.append('radiance')
        else:
            pass

        # Make sure UTC is in there
        if 'utc' not in columns_:
            columns_.append('utc')
        else:
            pass

        if len(columns_) != len(set(columns_)):
            columns_ = list(set(columns_))
        else:
            pass

        for col in columns_:
            if col not in self.data.columns:
                columns_.remove(col)
            else:
                pass

        subset = self.data[columns_]
        if filename.endswith('.csv'):
            subset.to_csv(filename)
        elif filename.endswith('.pkl'):
            subset.to_pickle(filename)
        elif filename.endswith('.html'):
            subset.to_html(filename)
        elif filename.endswith('.tex'):
            subset.to_latex(filename)
        else:
            print('Valid output formats = csv, pkl, html, tex')


