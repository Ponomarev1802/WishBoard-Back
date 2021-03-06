from user import views as user
from wish import views as wish
import migrations


def setup_routes(app):
    app.router.add_get('/user', user.GetUser, name='GetUser')
    app.router.add_post('/user', user.AddUser)
    app.router.add_post('/login', user.LoginUser)
    app.router.add_post('/logout', user.Logout)
    app.router.add_get('/followers', user.GetFollowers)
    app.router.add_get('/follows', user.GetFollows)
    app.router.add_post('/follows/{id}', user.EditFollow)

    app.router.add_post('/wish', wish.AddWish)
    app.router.add_post('/wish/{id}', wish.EditWish)
    app.router.add_get('/wish/{id}', wish.GetWishFull)
    app.router.add_get('/wish', wish.GetWish)



    ###only when installing app
    app.router.add_get("/migrate", migrations.Migrate)


