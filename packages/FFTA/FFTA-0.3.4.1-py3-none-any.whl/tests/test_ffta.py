import os
import sys
import pytest
import numpy as np
import h5py

sys.path.insert(0, '..')

import ffta
import pyUSID as usid


# Testing of standard process flow
class TestFFTA:
    ff_folder = r'tests/testdata'
    ff_file = r'tests/testdata/FF_H5.h5'

    def delete_old_h5(self):

        try:
            os.remove(self.ff_file)
            os.remove(self.ff_folder + '/tfp_fixed.csv')
            os.remove(self.ff_folder + '/shift.csv')
            os.remove(self.ff_folder + '/tfp_test.csv')
            print('###### Deleted old .h5 file')
        except:
            print('###### Error with old .h5 file')

    def test_load_data_files(self):
        self.delete_old_h5()
        h5_path, data_files, parm_dict = ffta.load.load_hdf.load_folder(folder_path=self.ff_folder)
        assert (len(data_files) == 8)
        assert (len(parm_dict.items()) == 22)
        assert (type(h5_path) == str)

    def test_load_FF(self):
        self.delete_old_h5()
        h5_path, data_files, parm_dict = ffta.load.load_hdf.load_folder(folder_path=self.ff_folder)
        h5_path = h5_path.replace('\\', '/')  # travis
        h5_avg = ffta.load.load_hdf.load_FF(data_files, parm_dict, h5_path)

        assert (h5_avg.shape == (1024, 16000))
        usid.USIDataset(h5_avg)

        h5_svd = ffta.analysis.svd.test_svd(h5_avg, show_plots=False)
        h5_rb = ffta.analysis.svd.svd_filter(h5_avg, clean_components=[0, 1, 2, 3, 4])
        assert (h5_rb.shape == (1024, 16000))
        assert (h5_rb.name == '/FF_Group/FF_Avg-SVD_000/Rebuilt_Data_000/Rebuilt_Data')  # in right spot

        ff = ffta.hdf_utils.process.FFtrEFM(h5_rb, override=True)
        ff.update_parm(roi=0.0007, n_taps=499, fit=True, filter_amplitude=True)
        ff.compute()
        ff.reshape()
        ffta.hdf_utils.process.save_CSV_from_file(ff)

        tfp = h5_rb.file['FF_Group/FF_Avg-SVD_000/Rebuilt_Data_000/Rebuilt_Data-Fast_Free_000/tfp']
        assert (tfp.shape == (8, 128))

        shift = h5_rb.file['FF_Group/FF_Avg-SVD_000/Rebuilt_Data_000/Rebuilt_Data-Fast_Free_000/shift']
        assert (shift.shape == (8, 128))

        inst_freq = h5_rb.file['FF_Group/FF_Avg-SVD_000/Rebuilt_Data_000/Rebuilt_Data-Fast_Free_000/Inst_Freq']
        assert (inst_freq.shape == (1024, 16000))

        h5_avg.file.close()

        self.delete_old_h5()

        return
