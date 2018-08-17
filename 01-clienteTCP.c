#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

#define MAX_MSG 1024

/*
 Cliente envia mensagem ao servidor e imprime resposta
 recebida do Servidor
 */

int main(int argc , char *argv[]){
	// variaveis
	int socket_desc;
	struct sockaddr_in servidor;
	char *mensagem;
	char resposta_servidor[MAX_MSG];
	int tamanho;
	char msg[1024];

	/*****************************************/
	/* Criando um socket */
	// AF_INET = ARPA INTERNET PROTOCOLS
	// SOCK_STREAM = orientado a conexao
    // 0 = protocolo padrao para o tipo escolhido -- TCP
	socket_desc = socket(AF_INET , SOCK_STREAM , 0);
     
	if (socket_desc == -1){
		printf("Nao foi possivel criar socket\n");
		return -1;	
	}

	/* Informacoes para conectar no servidor */
	// IP do servidor
	// familia ARPANET
	// Porta - hton = host to network short (2bytes)
	servidor.sin_addr.s_addr = inet_addr("192.168.1.222");
	servidor.sin_family = AF_INET;
	servidor.sin_port = htons( 80 );

	//Conectando no servidor remoto
	if (connect(socket_desc , (struct sockaddr *)&servidor , sizeof(servidor)) < 0){
		printf("Nao foi possivel conectar\n");
		return -1;
	}
	printf("Conectado no servidor\n");
	/*****************************************/


	/*******COMUNICAO - TROCA DE MENSAGENS **************/

	//Enviando uma mensagem
	/*mensagem = "GET / HTTP/1.1\r\n\r\n";
	if( send(socket_desc , mensagem , strlen(mensagem) , 0) < 0){
		printf("Erro ao enviar mensagem\n");
		return -1;
	}
	puts("Dados enviados\n");

	*/

	scanf("%s", msg);
	mensagem = msg;
	if( send(socket_desc , mensagem , strlen(mensagem) , 0) < 0){
                printf("Erro ao enviar mensagem\n");
                return -1;
        }

	//Recebendo resposta do servidor

	while (1){
		if( (tamanho = recv(socket_desc, resposta_servidor, MAX_MSG , 0)) < 0){
			printf("Falha ao receber resposta\n");
			return -1;
		}

		if(strcmp(resposta_servidor,"BYE") == 10) {
			puts(resposta_servidor);
			goto FIM;
		}		


		printf("Resposta recebida: ");
		resposta_servidor[tamanho] = '\0';
		puts(resposta_servidor);
		scanf("%s", msg);
		mensagem = msg;
	        if( send(socket_desc , mensagem , strlen(mensagem) , 0) < 0){
        	        printf("Erro ao enviar mensagem\n");
                	return -1;
		}
	}

	/*****************************************/
FIM:	close(socket_desc);



	printf("Cliente finalizado com sucesso!\n");
	return 0;
}
