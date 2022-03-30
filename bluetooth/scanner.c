// For compiling: cc scanner.c -lbluetooh -o scanner
// Executing: sudo ./scanner -h bluetoothDeviceName
#include <time.h>
#include <sys/time.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/hci_lib.h>

#define SERVER_PORT 12345
#define SERVER_ADDR "127.0.0.1"

#define MUESTRASREF 20 // Muestras totales deseadas para calcular valor de referencia
#define BUFFER 10
#define WINDOWSIZE BUFFER - 1

int compare(const void *a, const void *b);
void calcularMediana();     // Actualiza el array de medianas con el nuevo valor de mediana
int calcularValorMediano(); // Retorna el valor mediano de las muestras que tenga el array buffer en ese momento
int calcularMedia();
int calcularValorReferencia(int rssi, int flagMode);
int init_ble(le_set_scan_enable_cp *scan_cp); // Código necesario para iniciar escaneo
// Tamanho del buffer que se utilizara para calcular el valor de referencia
//  int muestras[MUESTRASREF] = {-28, -34, -29, -29, -30, -29, -33, -28, -90, -90, -30, -89, -28, -31, -28, -30, -93, -32, -30, -30};
//  int muestras[MUESTRASREF]={0}; // Buffer entrante de muestras para calcular valor referencia
int buffer[BUFFER] = {0};      // Buffer de llenado para calcular medianas para el valor de referencia
int bufferAux[BUFFER] = {0};   // Para ordenar el buffer y calcular las medianas
int medians[BUFFER + 1] = {0}; // Para guardar las diferentes medianas que vamos calculando
int valorRef = 0;              // Media de las medianas calculadas
int contMedians = 0;           // Contador auxiliar para controlar en que posicion guardamos las medianas

int contBufferRef = 0;  // Para rellenar buffer
int contMuestraRef = 0; // Contador de muestras: 0<x<=MUESTRASREF
int flagRefCalculada = 1;

// Socket global variables
struct sockaddr_in server;
int socketfd = -1;

int init_socket()
{
    if ((socketfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0)
    {
        printf("Error opening socket");
        exit(EXIT_FAILURE);
    }

    server.sin_family = AF_INET;
    server.sin_port = htons(SERVER_PORT);
    server.sin_addr.s_addr = inet_addr(SERVER_ADDR);

    printf("Socket created\n");
}

int socket_send(int value)
{
    char buffer[64];
    sprintf(buffer, "%i", value);
    printf("socket_send(): %s\n", buffer);
    return sendto(socketfd, buffer, (strlen(buffer) + 1), 0, (struct sockaddr *)&server, sizeof(server));
}

struct hci_request ble_hci_request(uint16_t ocf, int clen, void *status, void *cparam)
{
    struct hci_request rq;
    memset(&rq, 0, sizeof(rq));
    rq.ogf = OGF_LE_CTL;
    rq.ocf = ocf;
    rq.cparam = cparam;
    rq.clen = clen;
    rq.rparam = status;
    rq.rlen = 1;
    return rq;
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: -h bluetoothDeviceName\n");
        exit(EXIT_FAILURE);
    }

    const char *device_name = argv[2];
    printf("Device name: %s\n", device_name);

    struct timeval timestamp,start;
    gettimeofday(&start,NULL);

    // Init socket
    init_socket();
    le_set_scan_enable_cp scan_cp;
    int device = init_ble(&scan_cp);

    uint8_t buf[HCI_MAX_EVENT_SIZE];
    evt_le_meta_event *meta_event;
    le_advertising_info *info;
    int len;

    unsigned now = (unsigned)time(NULL);
    unsigned last_detection_time = now;
    int count = 0;

    // Keep scanning until we see nothing for 10 secs or we have seen lots of advertisements.  Then exit.
    // We exit in this case because the scan may have failed or stopped. Higher level code can restart
    printf("Starting scanning.....\n");
    while (1)
    {
        len = read(device, buf, sizeof(buf));
        if (len >= HCI_EVENT_HDR_SIZE)
        {
            meta_event = (evt_le_meta_event *)(buf + HCI_EVENT_HDR_SIZE + 1);
            if (meta_event->subevent == EVT_LE_ADVERTISING_REPORT)
            {
                uint8_t reports_count = meta_event->data[0];
                void *offset = meta_event->data + 1;
                while (reports_count--)
                {
                    info = (le_advertising_info *)offset;
                    char addr[18];
                    ba2str(&(info->bdaddr), addr);
                    int8_t rssi = (int8_t)info->data[info->length];
                    int flag = strncmp(&info->data[2], device_name, strlen(device_name)); // El nombre del dispositivo se encuentra en la posición 2

                    if (!flag)
                    {
                        // printf("Printing useful data:\n");
                        // printf("%s %d\n", addr, (int8_t)info->data[info->length]);
                        // printf("%.5s %d %s %i\n", &info->data[2], rssi, addr, info->bdaddr_type);
                        gettimeofday(&timestamp, NULL);
                        unsigned long timest = (timestamp.tv_sec-start.tv_sec) * 1000000 + (timestamp.tv_usec-start.tv_usec);
                        printf("RSSI received: %d %lu\n", rssi,timest);
                        count++;
                        last_detection_time = (unsigned)time(NULL);

                        // Mientras no tengamos un valor de referencia, entramos en el siguiente if hasta obtener dicho valor
                        if (valorRef == 0)
                        {
                            valorRef = calcularValorReferencia(rssi, 1);
                            if (valorRef != 0)
                                socket_send(valorRef);
                        }
                        // Una vez el valor de referencia está calculado siempre entraremos en el siguiente else, para calcular la mediana con las muestras entrantes
                        else
                        {
                            int mediana = calcularValorReferencia(rssi, 0);
                            // Si la mediana es 0, significa que todavía no se ha calculado
                            // Si no se ha calculado, significa que todavía no tiene las suficientes muestras
                            if (mediana != 0)
                            {
                                // printf("Mediana calculada con 10 muestras: %i\n",mediana);
                                socket_send(mediana);
                            }
                        }
                    }
                    offset = info->data + info->length + 2;
                }
            }
        }
        now = (unsigned)time(NULL);
    }
    // Disable scanning.

    memset(&scan_cp, 0, sizeof(scan_cp));
    scan_cp.enable = 0x00; // Disable flag.
    int ret, status;
    struct hci_request disable_adv_rq = ble_hci_request(OCF_LE_SET_SCAN_ENABLE, LE_SET_SCAN_ENABLE_CP_SIZE, &status, &scan_cp);
    ret = hci_send_req(device, &disable_adv_rq, 1000);
    if (ret < 0)
    {
        hci_close_dev(device);
        perror("Failed to disable scan.");
        return 0;
    }

    hci_close_dev(device);
    close(socketfd);

    return 0;
}

int init_ble(le_set_scan_enable_cp *scan_cp)
{
    int ret, status;

    // Get HCI device.
    int device = hci_open_dev(0);
    if (device < 0)
    {
        perror("Failed to open HCI device.");
        exit(1);
    }

    le_set_scan_parameters_cp scan_params_cp;
    memset(&scan_params_cp, 0, sizeof(scan_params_cp));
    scan_params_cp.type = 0x00;
    scan_params_cp.interval = htobs(0x0010);
    scan_params_cp.window = htobs(0x0010);
    scan_params_cp.own_bdaddr_type = 0x00;    // Public Device Address (default).
    scan_params_cp.filter = 0x00;             // Accept all.

    // Construimos una struc hci_request mediante el método ble_hci_request()
    struct hci_request scan_params_rq = ble_hci_request(OCF_LE_SET_SCAN_PARAMETERS, LE_SET_SCAN_PARAMETERS_CP_SIZE, &status, &scan_params_cp);

    ret = hci_send_req(device, &scan_params_rq, 1000);
    if (ret < 0)
    {
        hci_close_dev(device);
        perror("Failed to set scan parameters data.");
        exit(1);
    }

    // Set BLE events report mask.
    le_set_event_mask_cp event_mask_cp;
    memset(&event_mask_cp, 0, sizeof(le_set_event_mask_cp));
    int i = 0;
    for (i = 0; i < 8; i++)
        event_mask_cp.mask[i] = 0xFF;

    struct hci_request set_mask_rq = ble_hci_request(OCF_LE_SET_EVENT_MASK, LE_SET_EVENT_MASK_CP_SIZE, &status, &event_mask_cp);
    ret = hci_send_req(device, &set_mask_rq, 1000);
    if (ret < 0)
    {
        hci_close_dev(device);
        perror("Failed to set event mask.");
        exit(1);
    }

    // Enable scanning.
    memset(scan_cp, 0, sizeof(scan_cp));
    scan_cp->enable = 0x01;     // Enable flag.
    scan_cp->filter_dup = 0x00; // Filtering disabled.

    struct hci_request enable_adv_rq = ble_hci_request(OCF_LE_SET_SCAN_ENABLE, LE_SET_SCAN_ENABLE_CP_SIZE, &status, scan_cp);

    ret = hci_send_req(device, &enable_adv_rq, 1000);
    if (ret < 0)
    {
        hci_close_dev(device);
        perror("Failed to enable scan.");
        exit(1);
    }

    // Get Results.
    struct hci_filter nf;
    hci_filter_clear(&nf);
    hci_filter_set_ptype(HCI_EVENT_PKT, &nf);
    hci_filter_set_event(EVT_LE_META_EVENT, &nf);

    if (setsockopt(device, SOL_HCI, HCI_FILTER, &nf, sizeof(nf)) < 0)
    {
        hci_close_dev(device);
        perror("Could not set socket options\n");
        exit(1);
    }

    return device;
}

int compare(const void *a, const void *b)
{
    return (*(int *)a - *(int *)b);
}

void calcularMediana()
{
    memcpy(bufferAux, buffer, sizeof(buffer));
    qsort(bufferAux, BUFFER, sizeof(int), compare);
    if (BUFFER % 2 == 0)
        medians[contMedians] = (bufferAux[BUFFER / 2] + bufferAux[BUFFER / 2 + 1]) / 2;
    else
        medians[contMedians] = bufferAux[(BUFFER - 1) / 2];

    contMedians++;
}

int calcularValorMediano()
{
    int valorMediana = 0;
    memcpy(bufferAux, buffer, sizeof(buffer));
    qsort(bufferAux, BUFFER, sizeof(int), compare);
    if (BUFFER % 2 == 0)
        valorMediana = (bufferAux[BUFFER / 2] + bufferAux[BUFFER / 2 + 1]) / 2;
    else
        valorMediana = bufferAux[(BUFFER - 1) / 2];

    contMedians++;
    return valorMediana;
}

int calcularMedia()
{
    int acumulador = 0;
    for (int i = 0; i < BUFFER + 1; i++)
    {
        acumulador += medians[i];
    }
    return acumulador / (BUFFER + 1);
}

// if flagMode == 1 --> Referencia
// if flagMode == 0 --> Monitorizacion
int calcularValorReferencia(int rssi, int flagMode)
{
    int valorAuxiliarRetorno = 0;

    switch (flagMode)
    {

    case 0:
        // Llenamos buffer con muestras recibidas mientras contMuestrasRef <= WINDOWSIZE - 1,
        //                  Hasta que no recibimos las muestras necesarias (WINDOWSIZE), no calculamos la mediana
        if (contMuestraRef <= WINDOWSIZE - 1)
        {
            // 1. LLenamos buffer de referencia
            buffer[contBufferRef] = rssi;

            contBufferRef++;
            contMuestraRef++;
        }
        // Si el buffer se llena, contMuestraRef = WINDOWSIZE calculo la mediana con las muestras obtenidas en el buffer
        else
        {
            valorAuxiliarRetorno = calcularValorMediano();
            printf("\nValor mediano calculado: %i\n", valorAuxiliarRetorno);
            // printf("\nValor de referencia: %i\n", valorRef);
            memset(buffer, 0, sizeof(buffer));
            contBufferRef = 0;
            contMuestraRef = 0;
            // flagRefCalculada = 0;
        }

        break;
    case 1:
        // Case para calcular valor de referencia
        // Mientras que contMuestraRef sea menor o igual que MUESTRASREF (muestras totales necesarias para calcular valor de referencia)
        if (contMuestraRef <= MUESTRASREF - 1)
        {

            // 1. LLenamos buffer de referencia
            buffer[contBufferRef] = rssi;
            // 2. Compruebo si he llenado el buffer (contBufferRef == WINDOWSIZE)
            if (contBufferRef == WINDOWSIZE)
                // 2.1 Pongo contador a 0 para empezar a llenar de nuevo el buffer empezando en la posicion 0
                contBufferRef = 0;
            else
                // 2.2 Incremento contador del buffer de referencia
                contBufferRef++;
            // 3.Compruebo si he recibio las suficientes muestras como para calcular la mediana (al menos necesito N = MUESTRASREF / 2 - 1)
            //          Para nuestro caso, MUESTRASREF = 20 --> N = 20/2 - 1 = 9.
            //          Es decir, si contMuestraRef >= 9 (He recibido 10 muestras, 0 a la 9)
            //          Si se cumple esto, ya puedo calcular la mediana con 10 muestras
            if (contMuestraRef >= MUESTRASREF / 2 - 1)
                calcularMediana();
            // 4. Tras realizar todo el proceso, incremento el contador de muestras y espero a la siguiente iteración (llamada a la función con la siguiente muestra recibida)
            contMuestraRef++;
        }
        // contMuestraRef = MUESTRASREF lo que implica que he recibo las muestras suficientes para calcular la media de las medianas.
        //          (El buffer de medianas se ha llenado y estamos listos para calcular la media de las medianas calculadas para así retornar el valor de referencia).
        else
        {
            valorAuxiliarRetorno = calcularMedia();
            printf("\nValor de referencia: %i\n", valorAuxiliarRetorno);
            contBufferRef = 0;
            contMuestraRef = 0;
            contMedians = 0;
            memset(buffer, 0, sizeof(buffer));
            memset(medians, 0, sizeof(medians));
            // flagRefCalculada = 0;
        }
        break;
    default:
        break;
    }

    return valorAuxiliarRetorno;
}
