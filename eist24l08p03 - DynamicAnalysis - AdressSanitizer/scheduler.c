#include <stdio.h>
#include <unistd.h>
#include "include/minheap.h"

// Structure representing a process
typedef struct Process {
    int id;
    unsigned long runtime;
} Process;

// Gloabal Variables
Process *processes = NULL;

// Function to execute a process
void execute_process(struct Process *process) {
    // Simulate process execution time
    sleep(process->runtime / 10);
    printf("Process %d executed for %lu seconds\n", process->id, process->runtime);
}

Node *parse(int num_processes, char *argv[]) {
    // Allocate memory for the array of processes
    Node *nodes = (Node *) malloc(num_processes * sizeof(Node));

    // Checking if memory is allocated to nodes or not
    if (nodes == NULL) {
        printf("Memory error");
        return NULL;
    }

    // Extract the process ID and runtime from the command-line arguments
    processes = (Process *) malloc(num_processes * sizeof(Process));

    // Checking if memory is allocated to process or not
    if (processes == NULL) {
        printf("Memory error");
        free(nodes);
        return NULL;
    }

    char *endptr;
    for (int i = 0; i < num_processes; i++) {
        Process *process = &processes[i];
        process->id = (int) strtol(argv[2 * i + 1], &endptr, 10);
        if (*endptr != '\0') {
            printf("Invalid process ID: %s\n", argv[2 * i + 1]);
            free(nodes);
            free(processes);
            return NULL;
        }
        process->runtime = strtoul(argv[2 * i + 2], NULL, 10);
        nodes[i] = createNode(process->runtime, process);
    }

    return nodes;
}

int main(int argc, char *argv[]) {
    // Calculate the number of processes based on the command-line arguments
    int num_processes = (argc - 1) / 2;

    Node *nodes = parse(num_processes, argv);
    if (nodes == NULL) {
        return 1;
    }

    printf("Starting scheduling\n");
    Heap *hp = createHeap(num_processes, nodes);

    if (hp == NULL) {
        perror("Heap creation failed");
        free(nodes);
        return 1;
    }

    // Process the processes in priority order (based on virtual runtime)
    while (hp->size > 0) {
        // Get the process with the highest priority (minimum virtual runtime)
        Node min = extract_min(hp);
        if (min.data != NULL) {
            execute_process(min.data);
        }
    }

    printf("Printing summary\n");

    for (int i = 0; i < num_processes; i++) {
        Process *process = (Process *) nodes[i].data;
        if (process != NULL) {
            printf("Process[%d] ran for %lu seconds\n", process->id, process->runtime);
        }
    }

    free(processes);
    free(nodes);
    freeHeap(hp);

    return 0;
}
