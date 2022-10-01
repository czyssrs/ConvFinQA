

class parameters():

    prog_name = "generator"

    # set up your own path here
    root_path = "your project path"
    output_path = "your output path"
    cache_dir = "path to store downloaded models"

    model_save_name = "generator-bert-large-test"

    ### files from the retriever results
    train_file = root_path + "data/train_retrieve.json"
    valid_file = root_path + "data/dev_retrieve.json"
    test_file = root_path + "data/test_retrieve.json"

    op_list_file = "operation_list.txt"
    const_list_file = "constant_list.txt"

    # model choice: bert, roberta, albert
    pretrained_model = "bert"
    model_size = "bert-large-uncased"

    # # model choice: bert, roberta, albert
    # pretrained_model = "roberta"
    # model_size = "roberta-large"

    # single sent or sliding window
    # single, slide, gold, none
    retrieve_mode = "single"

    # use seq program or nested program
    program_mode = "seq"

    # mode: train or test
    device = "cuda"
    mode = "test"
    saved_model_path = output_path + "generator-bert-large-1_20220607160852/saved_model/loads/69/model.pt"
    build_summary = False

    sep_attention = True
    layer_norm = True
    num_decoder_layers = 1

    max_seq_length = 512 # 2k for longformer, 512 for others
    max_program_length = 30
    n_best_size = 20
    dropout_rate = 0.1

    batch_size = 16
    batch_size_test = 16
    epoch = 300
    learning_rate = 1e-5

    report = 300
    report_loss = 100

    max_step_ind = 11
