import configparser as cp
import tensorflow as tf
import pandas as pd
import numpy as np
import time
import xlrd
from xlutils.copy import copy

rb = xlrd.open_workbook('log.xls')
col = rb.sheet_by_index(0).ncols
print("cols: %d" % col)
wb = copy(rb)


def config_reader():
    config_dict = {}
    conf = cp.ConfigParser()
    conf.read("./config.ini")
    config_dict["max_steps"] = int(conf.get('ARG', 'MAX_STEPS'))
    config_dict["learning_rate"] = float(conf.get('ARG', 'LEARNING_RATE'))
    config_dict["data_dir"] = str(conf.get('ARG', 'DATA_DIR'))
    config_dict["batch_size"] = int(conf.get('ARG', 'BATCH_SIZE'))
    config_dict["timestep_size"] = int(conf.get('ARG', 'TIMESTEP_SIZE'))
    conf.clear()
    return config_dict


def get_data():
    config = config_reader()
    label = ['WTI', 'dollar', 'wti_index', 'wti_fut']
    stock = ['DDAIF_', 'F_', 'NSU.DE_']
    training_data = pd.read_excel(config["data_dir"], sheet_name='atrain')
    # training_data[['WTI', 'dollar', 'wti_index', 'wti_fut', 'DDAIF_close', 'DDAIF_pct', 'DDAIF_amt', 'DDAIF_open']]
    # label[0], label[1], label[2], label[3]
    x_train = training_data[[label[0], label[1], label[2], label[3], stock[0]+'close', stock[0]+'pct', stock[0]+'amt', stock[0]+'open']]
    x_train = np.array(x_train)
    x_train = x_train[:, :, np.newaxis]
    y_train = training_data[[stock[0]+'output1', stock[0]+'output2']]
    y_train = np.array(y_train)

    test_data = pd.read_excel(config["data_dir"], sheet_name='atest')
    x_test = test_data[[label[0], label[1], label[2], label[3], stock[0]+'close', stock[0]+'pct', stock[0]+'amt', stock[0]+'open']]
    x_test = np.array(x_test)
    y_test = test_data[[stock[0]+'output1', stock[0]+'output2']]
    y_test = np.array(y_test)
    y_test = y_test[0:521]
    temp = 0
    x_test_data = np.zeros((521, config["timestep_size"], x_train.shape[1]))
    for j in range(config['batch_size']):
        if config["timestep_size"] + temp > x_train.shape[0]:
            break
        timestepx = x_test[temp:config["timestep_size"] + temp]
        temp += 1
        x_test_data[j] = timestepx
        if temp > x_train.shape[0]:
            temp %= x_train.shape[0]
    x_test_data = x_test_data[:, :, :, np.newaxis]
    result = [x_train, y_train, x_test_data, y_test]
    return result


def lstm_train(input_data_x, input_data_y, test_data_x, test_data_y):
    config = config_reader()
    input_size = input_data_x.shape[1]
    timestep_size = config["timestep_size"]
    # layer_num = 2
    class_num = input_data_y.shape[1]

    keep_prob = tf.placeholder(tf.float32, [])
    with tf.name_scope('inputs'):
        x = tf.placeholder(tf.float32, [None, timestep_size, input_size, 1], name='x')
        y = tf.placeholder(tf.float32, [None, class_num], name='y')
        inputdata = tf.reshape(x, [-1, timestep_size, input_size])


    rnn_cell = tf.contrib.rnn.BasicLSTMCell(num_units=input_size, forget_bias=1.0, state_is_tuple=True)
    rnn_cell = tf.contrib.rnn.DropoutWrapper(cell=rnn_cell, input_keep_prob=1.0, output_keep_prob=keep_prob)
    # mrnn_cell = tf.contrib.rnn.MultiRNNCell([rnn_cell] * layer_num, state_is_tuple=True)
    outputs, final_state = tf.nn.dynamic_rnn(cell=rnn_cell, inputs=inputdata, initial_state=None, dtype=tf.float32,
                                             time_major=False)

    output = tf.layers.dense(inputs=outputs[:, -1, :], units=class_num)


    cross_entropy = tf.losses.softmax_cross_entropy(onehot_labels=y, logits=output)
    train_step = tf.train.AdamOptimizer(config['learning_rate']).minimize(cross_entropy)
    with tf.name_scope('accuracy'):
        correct_predict = tf.equal(tf.argmax(y, axis=1), tf.argmax(output, axis=1))
        accuracy = tf.reduce_mean(tf.cast(correct_predict, 'float'))

    sess = tf.Session()
    writer = tf.summary.FileWriter("lstmboard/", sess.graph)
    sess.run(tf.global_variables_initializer())
    batch_start = 0
    timestep_start = 0
    epoch = 1
    # row = 0
    for i in range(config['max_steps'] + 1):
        if config['batch_size'] + batch_start > input_data_x.shape[0]:
            epoch += 1
            batch_start = 0
        batchx = np.zeros((config['batch_size'], timestep_size, input_size))
        for j in range(config['batch_size']):
            if timestep_size + timestep_start > input_data_x.shape[0]:
                break
            timestepx = input_data_x[timestep_start:timestep_size + timestep_start]
            timestep_start += 1
            batchx[j][:, :, np.newaxis] = timestepx
            if timestep_start > input_data_x.shape[0]:
                timestep_start %= input_data_x.shape[0]
        batchx = batchx[:, :, :, np.newaxis]
        batchy = input_data_y[batch_start:config['batch_size'] + batch_start]
        batch_start += config['batch_size']
        if batch_start > input_data_x.shape[0]:
            batch_start %= input_data_x.shape[0]
        if (i + 1) % 100 == 0:
            train_accuracy = sess.run(accuracy, feed_dict={x: batchx, y: batchy, keep_prob: 1.0})
            loss = sess.run(cross_entropy, feed_dict={x: batchx, y: batchy, keep_prob: 1.0})
            print("epoch %d, step %d, training accuracy %g, loss %g" % (epoch, (i + 1), train_accuracy, loss))
            # train_accuracy = "%.6f" % float(train_accuracy)
            # wb.get_sheet(2).write(row, col, float(train_accuracy))
            # row += 1
        sess.run(train_step, feed_dict={x: batchx, y: batchy, keep_prob: 0.5})
    test_accuracy = sess.run(accuracy, feed_dict={x: test_data_x, y: test_data_y, keep_prob: 1.0})
    print("LSTM test accuracy %g" % test_accuracy)
    test_accuracy = "%.6f" % float(test_accuracy)
    wb.get_sheet(0).write(0, col, float(test_accuracy))
    sess.close()


def gru_train(input_data_x, input_data_y, test_data_x, test_data_y):
    config = config_reader()
    input_size = input_data_x.shape[1]
    timestep_size = config["timestep_size"]
    # layer_num = 2
    class_num = input_data_y.shape[1]

    keep_prob = tf.placeholder(tf.float32, [])
    with tf.name_scope('inputs'):
        x = tf.placeholder(tf.float32, [None, timestep_size, input_size, 1])
        y = tf.placeholder(tf.float32, [None, class_num])

        inputdata = tf.reshape(x, [-1, timestep_size, input_size])

    rnn_cell = tf.contrib.rnn.GRUCell(num_units=input_size)
    rnn_cell = tf.contrib.rnn.DropoutWrapper(cell=rnn_cell, input_keep_prob=1.0, output_keep_prob=keep_prob)
    # mrnn_cell = tf.contrib.rnn.MultiRNNCell([rnn_cell] * layer_num, state_is_tuple=True)

    outputs, final_state = tf.nn.dynamic_rnn(cell=rnn_cell, inputs=inputdata, initial_state=None, dtype=tf.float32,
                                             time_major=False)
    output = tf.layers.dense(inputs=outputs[:, -1, :], units=class_num)

    cross_entropy = tf.losses.softmax_cross_entropy(onehot_labels=y, logits=output)
    train_step = tf.train.AdamOptimizer(config['learning_rate']).minimize(cross_entropy)
    with tf.name_scope('accuracy'):
        correct_predict = tf.equal(tf.argmax(y, axis=1), tf.argmax(output, axis=1))
        accuracy = tf.reduce_mean(tf.cast(correct_predict, 'float'))

    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter("gruboard", sess.graph)
    batch_start = 0
    timestep_start = 0
    epoch = 1
    for i in range(config['max_steps'] + 1):
        if config['batch_size'] + batch_start > input_data_x.shape[0]:
            epoch += 1
            batch_start = 0
        batchx = np.zeros((config['batch_size'], timestep_size, input_size))
        for j in range(config['batch_size']):
            if timestep_size + timestep_start > input_data_x.shape[0]:
                break
            timestepx = input_data_x[timestep_start:timestep_size + timestep_start]
            timestep_start += 1
            batchx[j][:, :, np.newaxis] = timestepx
            if timestep_start > input_data_x.shape[0]:
                timestep_start %= input_data_x.shape[0]
        batchx = batchx[:, :, :, np.newaxis]
        batchy = input_data_y[batch_start:config['batch_size'] + batch_start]
        batch_start += config['batch_size']
        if batch_start > input_data_x.shape[0]:
            batch_start %= input_data_x.shape[0]
        # if (i + 1) % 100 == 0:
        #     train_accuracy = sess.run(accuracy, feed_dict={x: batchx, y: batchy, keep_prob: 1.0})
        #     loss = sess.run(cross_entropy, feed_dict={x: batchx, y: batchy, keep_prob: 1.0})
        #     print("epoch %d, step %d, training accuracy %g, loss %g" % (epoch, (i + 1), train_accuracy, loss))
        sess.run(train_step, feed_dict={x: batchx, y: batchy, keep_prob: 0.5})
    test_accuracy = sess.run(accuracy, feed_dict={x: test_data_x, y: test_data_y, keep_prob: 1.0})
    print("GRU test accuracy %g" % test_accuracy)
    test_accuracy = "%.6f" % float(test_accuracy)
    wb.get_sheet(0).write(1, col, float(test_accuracy))
    sess.close()


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding="VALID")


def max_pool(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 1, 1], strides=[1, 2, 1, 1], padding="VALID")


def cnn_train(input_data_x, input_data_y, test_data_x, test_data_y):
    config = config_reader()
    input_size = input_data_x.shape[1]
    timestep_size = config["timestep_size"]
    class_num = input_data_y.shape[1]

    with tf.name_scope('inputs'):
        x = tf.placeholder(tf.float32, [None, timestep_size, input_size, 1])
        y = tf.placeholder(tf.float32, [None, class_num])

        inputdata = tf.reshape(x, [-1, timestep_size, input_size, 1])

    with tf.name_scope('convolution'):
        W_conv1 = weight_variable([1, input_size, 1, 8])  # kernel_size , x, filter_size
        b_conv1 = bias_variable([8])  # filter_size
        h_conv1 = tf.nn.relu(conv2d(inputdata, W_conv1) + b_conv1)
        with tf.name_scope('max_pool'):
            h_pool1 = max_pool(h_conv1)
    with tf.name_scope('connection_layer'):
        temp = int(timestep_size // 2)
        W_fc1 = weight_variable([1 * temp * 8, 16])
        b_fc1 = bias_variable([16])
        h_pool2_flat = tf.reshape(h_pool1, [-1, 1 * temp * 8])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
        with tf.name_scope('dropout'):
            keep_prob = tf.placeholder(tf.float32)
            h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    with tf.name_scope('softmax'):
        W_fc2 = weight_variable([16, class_num])
        b_fc2 = bias_variable([class_num])
        output = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    with tf.name_scope('loss'):
        cross_entropy = tf.losses.softmax_cross_entropy(onehot_labels=y, logits=output)
    train_step = tf.train.AdamOptimizer(config['learning_rate']).minimize(cross_entropy)
    with tf.name_scope('accuracy'):
        correct_predict = tf.equal(tf.argmax(y, axis=1), tf.argmax(output, axis=1))
        accuracy = tf.reduce_mean(tf.cast(correct_predict, 'float'))

    init = tf.global_variables_initializer()
    sess = tf.InteractiveSession()
    writer = tf.summary.FileWriter("cnnboard/", sess.graph)
    sess.run(init)
    batch_start = 0
    timestep_start = 0
    epoch = 1
    for i in range(config['max_steps'] + 1):
        if config['batch_size'] + batch_start > input_data_x.shape[0]:
            epoch += 1
            batch_start = 0
        batchx = np.zeros((config['batch_size'], timestep_size, input_size))
        for j in range(config['batch_size']):
            if timestep_size + timestep_start > input_data_x.shape[0]:
                break
            timestepx = input_data_x[timestep_start:timestep_size + timestep_start]
            timestep_start += 1
            batchx[j][:, :, np.newaxis] = timestepx
            if timestep_start > input_data_x.shape[0]:
                timestep_start %= input_data_x.shape[0]
        batchx = batchx[:, :, :, np.newaxis]
        batchy = input_data_y[batch_start:config['batch_size'] + batch_start]
        batch_start += config['batch_size']
        if batch_start > input_data_x.shape[0]:
            batch_start %= input_data_x.shape[0]
        # if (i + 1) % 100 == 0:
        #     train_accuracy = sess.run(accuracy, feed_dict={x: batchx, y: batchy, keep_prob: 1.0})
        #     loss = sess.run(cross_entropy, feed_dict={x: batchx, y: batchy, keep_prob: 1.0})
        #     print("epoch %d, step %d, training accuracy %g, loss %g" % (epoch, (i + 1), train_accuracy, loss))
        sess.run(train_step, feed_dict={x: batchx, y: batchy, keep_prob: 0.5})
    test_accuracy = sess.run(accuracy, feed_dict={x: test_data_x, y: test_data_y, keep_prob: 1.0})
    print("CNN test accuracy %g" % test_accuracy)
    test_accuracy = "%.6f" % float(test_accuracy)
    wb.get_sheet(0).write(2, col, float(test_accuracy))
    sess.close()


if __name__ == '__main__':
    data = get_data()

    start = time.clock()
    lstm_train(data[0], data[1], data[2], data[3])
    end = time.clock()
    print("LSTM running time: %g s" % (end - start))
    t = "%.4f" % (end - start)
    wb.get_sheet(1).write(col, 0, float(t))

    # start = time.clock()
    # gru_train(data[0], data[1], data[2], data[3])
    # end = time.clock()
    # print("GRU running time: %g s" % (end - start))
    # t = "%.5f" % (end - start)
    # wb.get_sheet(1).write(col, 1, float(t))

    # start = time.clock()
    # cnn_train(data[0], data[1], data[2], data[3])
    # end = time.clock()
    # print("CNN running time: %g s" % (end - start))
    # t = "%.4f" % (end - start)
    # wb.get_sheet(1).write(col, 2, float(t))

    wb.save('log.xls')
