#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
	char msg[50];
	char buffer[50];
	int buffer1;
	int fileids[2], fileids1[2];

	/*Create pipes with no errors*/
	if (pipe(fileids) == 0 && pipe(fileids1) == 0)

		if (fork() == 0){	/* Child Process */
			close(fileids[0]); /* Fecha o descritor de leitura*/
			close(fileids1[1]);	/* Fecha o descritor de escrita*/

			read (fileids1[0], &buffer1, sizeof(buffer1)); /* Le do fileids1 e mete no buffer1*/
			printf("Received from pipe the message: %d\n",buffer1);
			close(fileids1[0]); /*Fechar descritor de leitura*/

			if (getppid() != buffer1){
				printf("PID sent by father is wrong!\n");
			}

			sprintf(msg, "Hello father, my PID is %d", getpid());
			write (fileids[1], msg, sizeof(msg)); /**/
			close(fileids[1]); /* Fecha o descritor de escrita*/

		}
		else{
			/* Processo Pai */
			close(fileids[1]);	/* Fecha o descritor de escrita*/
			close(fileids1[0]);	/* Fecha o descritor de leitura*/

			int pid_pai = getpid();
			write (fileids1[1], &pid_pai, sizeof(int));
			close(fileids1[1]);

			read (fileids[0], buffer, sizeof(buffer));
			printf("Received from father the PID: %s\n",buffer);
			close(fileids[0]); /* Fecha o descritor de leitura*/
		}
	else
		printf("Error creating pipe!\n");
	exit(0);
}
