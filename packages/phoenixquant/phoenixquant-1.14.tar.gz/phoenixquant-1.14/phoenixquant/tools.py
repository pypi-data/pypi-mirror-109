def to_backtrader(df):
    """ 将数据转换为 Backtrader Data Feed """
    return df.rename(columns={"open_interest": "openinterest"}, inplace=True)
