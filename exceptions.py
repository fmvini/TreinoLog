
class TreinoLogError(Exception):
    pass


class RegistroNaoEncontradoError(TreinoLogError):
    pass


class RegraDeNegocioError(TreinoLogError):
    pass
