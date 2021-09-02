from sklearn.neural_network import MLPClassifier
import random
import pickle


def get_class(values):
    total = 0
    for n in values:
        total = total + n
    if total > 0.66:
        return 1
    return 0

def generate_input(size):
    i = []
    for _ in range(0, size):
        i.append(random.random())
    return i


mlp = MLPClassifier(
    alpha=1e-05,
    hidden_layer_sizes=(40, 40),
    random_state=1,
    solver='lbfgs')

SIZE = 2
x = [ generate_input(SIZE) for _ in range(0, 100000) ]
y = [ get_class(i) for i in x ]

mlp.fit(x, y)

x_test = [ generate_input(SIZE) for _ in range(0, 10000) ]
results = mlp.predict(x_test)

correct = 0
incorrect = 0
for i in range(0, len(x_test)):
    inputs = x_test[i]
    expected = get_class(inputs)
    actual = results[i]
    if expected == actual:
        correct = correct + 1
    else:
        incorrect = incorrect + 1

print(correct)
print(incorrect)
print(correct / (correct + incorrect))


### Test model persistance ###
model_path = './models/2_input_sum_greater_than_half'
pickle.dump(mlp, open(model_path, 'wb'))
reloaded_model = pickle.load(open(model_path, 'rb'))
results = reloaded_model.predict(x_test)

correct = 0
incorrect = 0
for i in range(0, len(x_test)):
    inputs = x_test[i]
    expected = get_class(inputs)
    actual = results[i]
    if expected == actual:
        correct = correct + 1
    else:
        incorrect = incorrect + 1

print(correct)
print(incorrect)
print(correct / (correct + incorrect))
