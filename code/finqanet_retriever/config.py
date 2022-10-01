

class parameters():

    prog_name = "retriever"

    # set up your own path here
    root_path = "your project path"
    output_path = "your output path"
    cache_dir = "path to store downloaded models"

    # the name of your result folder.
    model_save_name = "retriever-roberta-large-2e-5-new-test"

    # use "train_turn.json", "dev_turn.json", and "test_turn.json"
    train_file = root_path + "data/train_turn.json"
    valid_file = root_path + "data/dev_turn.json"
    test_file = root_path + "data/test_turn.json"

    op_list_file = "operation_list.txt"
    const_list_file = "constant_list.txt"

    # model choice: bert, roberta
    # pretrained_model = "bert"
    # model_size = "bert-base-uncased"

    pretrained_model = "roberta"
    model_size = "roberta-large"

    # mode: train or test
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
