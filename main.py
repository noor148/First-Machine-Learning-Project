import pandas as pd
import SVM
DIM = 8


def give_me_grid():
    p = {}
    for i in range(DIM * DIM):
        p[i] = [1]
    return pd.DataFrame.from_dict(p)

def main():
    model = SVM.train_model()
    print(model.predict(give_me_grid())[0])

if __name__ == "__main__":
    main()
