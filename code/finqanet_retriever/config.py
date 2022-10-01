

class parameters():

    prog_name = "retriever"

    # set up your own path here
    root_path = "/mnt/george_bhd/zhiyuchen/FinDial/"
    output_path = "/mnt/george_bhd/zhiyuchen/findial_output/"
    cache_dir = "/mnt/george_bhd/zhiyuchen/misc_cache/"

    # the name of your result folder.
    model_save_name = "retriever-roberta-large-2e-5-new-test"

    train_file = root_path + "data/raw/final/train_turn.json"
    valid_file = root_path + "data/raw/final/dev_turn.json"

    test_file = root_path + "data/raw/final/test_turn.json"

    op_list_file = "operation_list.txt"
    const_list_file = "constant_list.txt"

    # model choice: bert, roberta
    # pretrained_model = "bert"
    # model_size = "bert-base-uncased"

    pretrained_model = "roberta"
    model_size = "roberta-large"

    # train or test
    device = "cuda"
    mode = "test"
    resume_model_path = ""

    ### to load the trained model in test time
    saved_model_path = output_path + \
        "retriever-roberta-large-2e-5-new_20220504055555/saved_model/loads/10/model.pt"
    build_summary = False

    option = "rand"
    neg_rate = 3
    topn = 5

    sep_attention = True
    layer_norm = True
    num_decoder_layers = 1

    max_seq_length = 512
    max_program_length = 100
    n_best_size = 20
    dropout_rate = 0.1

    batch_size = 16
    batch_size_test = 16
    epoch = 100
    learning_rate = 2e-5

    report = 300
    report_loss = 100
