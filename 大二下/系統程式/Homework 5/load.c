#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ESTAB 100

typedef struct {
    char name[10];
    int address;
} ESTAB_Entry;

ESTAB_Entry estab[MAX_ESTAB];
int estab_count = 0;

int search_estab(char* name) {
    for(int i = 0; i < estab_count; i++) {
        if(strcmp(estab[i].name, name) == 0) return 1;
    }
    return 0;
}

void insert_estab(char* name, int address) {
    strcpy(estab[estab_count].name, name);
    estab[estab_count].address = address;
    estab_count++;
}

void trim_spaces(char* str) {
    char *p = strchr(str, ' ');
    if (p) *p = '\0';
    int len = strlen(str);
    while(len > 0 && (str[len-1] == '\n' || str[len-1] == '\r')) {
        str[len-1] = '\0';
        len--;
    }
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("Syntax: %s <address> <file 1> <file 2> ...\n", argv[0]);
        return 1;
    }

    int PROGADDR = (int)strtol(argv[1], NULL, 16);
    int CSADDR = PROGADDR;
    int CSLTH = 0;

    printf("Control\t\tSymbol\n");
    printf("section\t\tname\t\tAddress\t\tLength\n");
    printf("------------------------------------------------------\n");

    for (int i = 2; i < argc; i++) {
        FILE *fp = fopen(argv[i], "r");
        if (!fp) {
            printf("Error: Cannot open file %s\n", argv[i]);
            continue;
        }

        char line[256];
        while (fgets(line, sizeof(line), fp)) {
            if (line[0] == 'H') {
                char cs_name[7] = {0};
                unsigned int length = 0;

                if (sscanf(line, "H%6s%*6x%6x", cs_name, &length) != 2) {
                    printf("Error: Invalid header record format\n");
                    continue;
                }

                CSLTH = (int)length;

                if (search_estab(cs_name)) {
                    printf("Error: Duplicate external symbol %s\n", cs_name);
                } else {
                    insert_estab(cs_name, CSADDR);
                    printf("%-10s\t\t\t%04X\t\t%04X\n", cs_name, CSADDR, CSLTH);
                }
            } 
            else if (line[0] == 'D') {
                int offset = 1;
                while (line[offset] != '\0' && line[offset] != '\n' && line[offset] != '\r') {
                    char sym_name[7] = {0};
                    char sym_addr_str[7] = {0};
                    int consumed = 0;

                    if (sscanf(line + offset, "%6s%6s%n", sym_name, sym_addr_str, &consumed) != 2) {
                        break;
                    }
                    if (consumed <= 0) {
                        break;
                    }
                    offset += consumed;

                    int sym_addr = (int)strtol(sym_addr_str, NULL, 16);

                    if (search_estab(sym_name)) {
                        printf("Error: Duplicate external symbol %s\n", sym_name);
                    } else {
                        int abs_addr = CSADDR + sym_addr;
                        insert_estab(sym_name, abs_addr);
                        printf("\t\t%-10s\t%04X\n", sym_name, abs_addr);
                    }
                }
            } 
            else if (line[0] == 'E') {
                break; 
            }
        }
        
        CSADDR += CSLTH;
        fclose(fp);
    }

    return 0;
}