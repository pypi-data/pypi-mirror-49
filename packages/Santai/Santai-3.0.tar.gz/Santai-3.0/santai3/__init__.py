__author__ = 'Administrator'
'''import tensorflow as tf
state = tf.Variable(0.0,dtype=tf.float32)
one = tf.constant(1.0,dtype=tf.float32)
new_val = tf.add(state, one)
update = tf.assign(state, new_val)
init = tf.initialize_all_variables()
#print(state)
with tf.Session() as sess:
    sess.run(init)
    for _ in range(10):
        s=sess.run(state)
        u = sess.run([update])
        print(s)
        print(u)
#print(state)'''