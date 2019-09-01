def row2dict(row):
    return dict([(column.name, getattr(row, column.name)) for column in row.__table__.columns])
