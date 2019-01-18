from user import views as user
import migrations


def setup_routes(app):
    app.router.add_get('/getUser', user.getUser)
    app.router.add_post('/newUser', user.newUser)
    app.router.add_get('/newUser', user.newUser)
    app.router.add_get('/login', user.loginUser, name='login')
    app.router.add_post('/login', user.loginUser)
    app.router.add_post('/addWish', user.addWish)


    ###only when installing app
    app.router.add_get("/migrate", migrations.Migrate)

