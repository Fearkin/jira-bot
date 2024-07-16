from aiogram import Router


def setup_routers() -> Router:
    """Sets up routers from files in that directory. Order DOES matter!"""
    from . import ticket, admin, message_edit, user, unsupported_reply

    router = Router()
    router.include_router(admin.router)
    router.include_router(message_edit.router)
    router.include_router(ticket.router)
    router.include_router(user.router)
    router.include_router(unsupported_reply.router)

    return router
