#!/bin/sh
#   Este script inicializa as aplicacoes no docker
#   Se faz necessária uma variavel de ambiente de nome ENVIRONMENT com um dos seguintes valores:
# development, production

#   Quando nao existir a variavel de ambiente ENVIRONMENT o script seta automaricamente como "development"
if [ -z "${ENVIRONMENT}" ]
then
        ENVIRONMENT="development"
fi

# DOCKER ENTRYPOINT GIVE US THE EXECUTION FILE AS PARAMETER
APP="/usr/bin/supervisord"

#
# PEGA O ARQUIVO COM OS VALORES DE VARIAVEIS DE AMBIENTE DE PRODUCAO
#
f_run() {
    # RUN APP
    echo "RUNNING APP WITH:"
    echo "${APP}"
    ${APP}
}


#
# DO NOT CHANGE THE CODE BELOW
#
echo -ne "\n\n##\n##\tRUNNING WITH APP_ENVIRONMENT=\"${APP_ENVIRONMENT}\"\n##\n\n"
f_run
