import h5py
from bilby_pe import run


for i in range(0,params['tot_dataset_size'],params['tset_split']):

    _, signal_train, signal_train_pars,snrs = run(sampling_frequency=params['ndata']/params['duration'],
                                                        duration=params['duration'],
                                                        N_gen=params['tset_split'],
                                                        ref_geocent_time=params['ref_geocent_time'],
                                                        bounds=bounds,
                                                        fixed_vals=fixed_vals,
                                                        rand_pars=params['rand_pars'],
                                                        seed=params['training_data_seed']+i,
                                                        label=params['run_label'],
                                                        training=True)

    print("Generated: %s/data_%d-%d.h5py ..." % (params['train_set_dir'],(i+params['tset_split']),params['tot_dataset_size']))

    hf = h5py.File('%s/data_%d-%d.h5py' % (params['train_set_dir'],(i+params['tset_split']),params['tot_dataset_size']), 'w')
    for k, v in params.items():
        try:
            hf.create_dataset(k,data=v)
        except:
            pass
    hf.create_dataset('x_data', data=signal_train_pars)
    for k, v in bounds.items():
        hf.create_dataset(k,data=v)
    hf.create_dataset('y_data_noisy', data=signal_train)
    hf.create_dataset('y_data_noisefree', data=signal_train)
    #hf.create_dataset('rand_pars', data=np.string_(params['rand_pars']))
    hf.create_dataset('snrs', data=snrs)
    hf.close()