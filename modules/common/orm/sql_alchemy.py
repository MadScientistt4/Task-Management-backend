from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase

# When the class definition is completed, a new Table and mapper() will have been generated.


"""class SQLAlchemy(SQLAlchemyBase):

    def __init__(self, database_url=None, connect_args={}, autoflush=False, autocommit=False, **kwargs):
        
        :param engine: SQLAlchemy engine created with `create_engine` function
        
        if database_url is not None:
            # TODO:  take connect_args from method arguments
            # connect_args={'sslmode':'require'} For SSL enforcement
            engine = create_engine(database_url, connect_args={'sslmode': 'require'})
            self.session = scoped_session(sessionmaker(autocommit=autocommit,  autoflush=autoflush, bind=engine))
        super().__init__(**kwargs)
"""