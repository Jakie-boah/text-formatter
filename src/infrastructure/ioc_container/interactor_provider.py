from dishka import Provider, Scope, provide
from src.application.interactors.text_format_interactor import TextInteractor


class InteractorProvider(Provider):
    text_format_interactor = provide(TextInteractor, scope=Scope.REQUEST)
