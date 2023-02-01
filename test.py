import biomage_programmatic_interface as bpi

c = bpi.Connection('stefan@biomage.net', 'Fu2.QAG}', 'local')
exp = c.create_experiment('molq te raboti')
exp.upload_samples('../../../sample1')
# exp_clone = exp.clone('0251e46d-02eb-4eff-a64f-a5ce9ed44d40')
exp.run()