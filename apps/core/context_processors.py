"""
Context processors para templates.
Inyecta la empresa actual en todos los templates.
"""


def empresa_context(request):
    return {
        'empresa': getattr(request, 'tenant', None),
    }
