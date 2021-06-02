import models as m


m.db.drop_tables({m.Course, m.Task, m.User, m.Week})
m.db.create_tables({m.Course, m.Task, m.User, m.Week})