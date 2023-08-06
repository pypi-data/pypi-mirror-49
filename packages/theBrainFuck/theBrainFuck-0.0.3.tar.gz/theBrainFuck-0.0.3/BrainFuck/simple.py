import numpy as np
import pandas as pd
from sklearn import metrics


class Data(object):
    def __init__(self, train, test, ID, TARGET, params={}):
        if 'drop' in params:
            train.drop(columns=params['drop'], inplace=True)
            test.drop(columns=params['drop'], inplace=True)
            print("Drop Columns Complete")
        self.train = train
        self.test = test
        self.ID = ID
        self.TARGET = TARGET

class Model(object):
    def __init__(self, DATA, MODEL='ETR', PARAMS={}, TEST_SIZE=0.25, RANDOM_STATE=5):
        from sklearn import model_selection
        col = [c for c in DATA.TRAIN.columns if c not in [DATA.ID, DATA.TARGET]]
        X1, X2, Y1, Y2 = model_selection.train_test_split(DATA.TRAIN[col], DATA.TRAIN[DATA.TARGET], test_size=TEST_SIZE,
                                                          random_state=RANDOM_STATE)
        if MODEL in ['ETR']:
            from sklearn import ensemble
            LIB = ensemble.ExtraTreesRegressor(n_jobs=-1, random_state=RANDOM_STATE)
            PARAMS_ = LIB.get_params()
            for p in PARAMS:
                if p in PARAMS_:
                    LIB.set_params({p: PARAMS[p]})
            LIB.fit(DATA.TRAIN[col], DATA.TRAIN[DATA.TARGET])
            DATA.TEST[DATA.TARGET] = LIB.predict(DATA.TEST[col])
            self.PRED = DATA.TEST[[DATA.ID, DATA.TARGET]]
        elif MODEL in ['XGB']:
            import xgboost as xgb
            default_params = {'num_round': 20, 'verbose_eval': 10, 'early_stopping_rounds': 20}

            if PARAMS == {}:
                PARAMS = {'eta': 0.2, 'max_depth': 4, 'objective': 'reg:linear', 'eval_metric': 'rmse',
                          'seed': RANDOM_STATE, 'silent': True, 'num_round': 20, 'verbose_eval': 10,
                          'early_stopping_rounds': 20}
            if 'num_round' in PARAMS:
                default_params['num_round'] = PARAMS['num_round']
            if 'verbose_eval' in PARAMS:
                default_params['verbose_eval'] = PARAMS['verbose_eval']
            if 'early_stopping_rounds' in PARAMS:
                default_params['early_stopping_rounds'] = PARAMS['early_stopping_rounds']

            def xgb_rmse(preds, y):
                y = y.get_label()
                score = np.sqrt(metrics.mean_squared_error(y, preds))
                return 'RMSE', score

            watchlist = [(xgb.DMatrix(X1, Y1), 'train'), (xgb.DMatrix(X2, Y2), 'valid')]
            LIB = xgb.train(PARAMS, xgb.DMatrix(X1, Y1), default_params['num_round'], watchlist,
                            verbose_eval=default_params['verbose_eval'], early_stopping_rounds=default_params[
                    'early_stopping_rounds'])  # feval=xgb_rmse, maximize=False
            DATA.TEST[DATA.TARGET] = LIB.predict(xgb.DMatrix(DATA.TEST[col]), ntree_limit=LIB.best_ntree_limit)
            self.PRED = DATA.TEST[[DATA.ID, DATA.TARGET]].copy()

        elif MODEL in ['LGB']:
            import lightgbm as lgb
            default_params = {'verbose_eval': 10}

            if PARAMS == {}:
                PARAMS = {'learning_rate': 0.2, 'max_depth': 7, 'boosting': 'gbdt', 'objective': 'regression',
                          'metric': 'rmse', 'seed': RANDOM_STATE, 'num_iterations': 100, 'early_stopping_round': 20}
            if 'verbose_eval' in PARAMS:
                default_params['verbose_eval'] = PARAMS['verbose_eval']

            def lgb_rmse(preds, y):
                y = np.array(list(y.get_label()))
                score = np.sqrt(metrics.mean_squared_error(y, preds))
                return 'RMSE', score, False

            LIB = lgb.train(PARAMS, lgb.Dataset(X1, label=Y1), valid_sets=lgb.Dataset(X2, label=Y2),
                            verbose_eval=default_params['verbose_eval'])  # feval=lgb_rmse
            DATA.TEST[DATA.TARGET] = LIB.predict(DATA.TEST[col], num_iteration=LIB.best_iteration)
            self.PRED = DATA.TEST[[DATA.ID, DATA.TARGET]].copy()

        elif MODEL in ['CB']:
            from catboost import CatBoostRegressor
            default_params = {'iterations': 100, 'learning_rate': 0.2, 'depth': 7, 'loss_function': 'RMSE',
                              'eval_metric': 'RMSE', 'od_type': 'Iter', 'od_wait': 20, 'verbose': False}

            if PARAMS == {}:
                PARAMS = {'iterations': 100, 'learning_rate': 0.2, 'depth': 7, 'loss_function': 'RMSE',
                          'eval_metric': 'RMSE', 'od_type': 'Iter', 'od_wait': 20, 'verbose': False}
            for p in default_params:
                if p not in PARAMS:
                    PARAMS[p] = default_params[p]

            LIB = CatBoostRegressor(iterations=PARAMS['iterations'], learning_rate=PARAMS['learning_rate'],
                                    depth=PARAMS['depth'], loss_function=PARAMS['loss_function'],
                                    eval_metric=PARAMS['eval_metric'], random_seed=RANDOM_STATE,
                                    od_type=PARAMS['od_type'], od_wait=PARAMS['od_wait'])
            LIB.fit(X1, Y1, eval_set=(X2, Y2), use_best_model=True, verbose=PARAMS['verbose'])
            DATA.TEST[DATA.TARGET] = LIB.predict(DATA.TEST[col])
            self.PRED = DATA.TEST[[DATA.ID, DATA.TARGET]].copy()

        else:
            DATA.TEST[DATA.TARGET] = np.median(DATA.TRAIN[DATA.TARGET])
            self.PRED = DATA.TEST[[DATA.ID, DATA.TARGET]].copy()


class Blend(object):
    def __init__(self, FILES=[], ID='id', TARGET='target', NAME='blend01.csv'):
        FILES_ = []
        i = 1
        for f in FILES:
            df = pd.read_csv(f, index_col=[ID]).rename(columns={TARGET: 'dp' + str(i)})
            FILES_.append(df)
            i += 1
        df = pd.concat(FILES_, sort=False, axis=1)
        df[TARGET] = df.sum(axis=1)
        df[TARGET] /= len(FILES_)
        self.BLEND = df
        BLEND = df[[TARGET]]
        BLEND.to_csv(NAME)
