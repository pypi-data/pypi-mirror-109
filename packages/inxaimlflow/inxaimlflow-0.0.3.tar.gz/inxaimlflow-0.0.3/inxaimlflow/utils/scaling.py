from sklearn.preprocessing import MinMaxScaler


def minmax(df, scale=(-1, 1)):
    min_max_scaler = MinMaxScaler(feature_range=scale)
    # Stack everything into a single column to scale by the global min / max
    tmp = df.to_numpy().reshape(-1, 1)
    return min_max_scaler.fit_transform(tmp).reshape(len(df), df.shape[1])