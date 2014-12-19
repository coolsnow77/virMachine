/**
 * Progname Name: vCpu.c
 *
 * Compile: gcc -o  vCpu vCpu.c  -lvirt
 */


/**
 * Program Name: vCpu.c
 * Author: steptodream
 * Description:A simple plugin to get vps cpu usage
 *             for nagios(nrpe) by libvirt api
 * Compile:gcc -o vCpu vCpu.c -lvirt
 */
#include <stdlib.h>
#include <stdio.h>
#include <libvirt/libvirt.h>
 
/* define the exit status for nagios */
#define OK       0
#define WARNING  1
#define CRITICAL 2
#define UNKNOWN  3
 
/* get cpu time of the given name */
double getCpuTime(char *vpsName,virConnectPtr conn) {
    virDomainInfo info;
    virDomainPtr domain = NULL;
    int ret;
 
    /* Find the domain of the given name */
    domain = virDomainLookupByName(conn, vpsName);
    if (domain == NULL) {
        printf("Failed to find the vps called %s\n", vpsName);
        exit(OK);
    }
 
    /* Get the information of the domain */
    ret = virDomainGetInfo(domain, &info);
    virDomainFree(domain);
 
    if (ret < 0) {
        printf("Failed to get information for %s\n", vpsName);
        exit(OK);
    }
 
    return info.cpuTime;
}
 
int main(int argc,char * argv[])
{
    char *vpsName;             /* vps name */
    int  interval = 1;         /* check interval */
    double warning;            /* warning value */
    double critical;           /* critical value */
    double cpuUsage;           /* cpu usage of the vps */
    struct timeval startTime;  /* time of the first time to get cpu time */
    struct timeval endTime;    /* time of the second time to get cpu time */
    int realTime;              /* real interval between two times */
    long long startCpuTime;    /* cpu time of the first time */
    long long endCpuTime;      /* cpu time of the second time */
    int  cpuTime;              /* value of startCpuTime - endCpuTime */
    char *output;              /* output data for nagios */
    int  ret;                  /* exit status for nagios */
    virConnectPtr conn;        /* connection pointer */
 
    switch (argc){
        case 5:
             interval = atoi(argv[4]);
        case 4:
             vpsName  = argv[1];
             warning  = atof(argv[2]);
             critical = atof(argv[3]);
             break;
        default:
             printf("Usage:vCpu <vName> <warning> <critical> [interval]\n\n");
             return OK;
    }
 
    /* connect to local Xen Host */
    conn = virConnectOpenReadOnly(NULL);
    if (conn == NULL) {
        printf("Failed to connect to local Xen Host\n");
        return OK;
    }
 
    /* get cpu time the first time */
    startCpuTime = getCpuTime(vpsName, conn);
 
    /* get start time */
    if (gettimeofday(&startTime, NULL) == -1) {
        printf("Failed to get start time\n");
        return OK;
    }
 
    /* wait for some seconds  */
    sleep(interval);
 
    /* get cpu time the second time */
    endCpuTime = getCpuTime(vpsName, conn);
 
    /* get end time */
    if (gettimeofday(&endTime, NULL) == -1) {
        printf("Failed to get end time\n");
        return OK;
    }
 
    /* colose connection */
    virConnectClose(conn);
 
    /* calculate the usage of cpu */
    /*  cpuTime: ns  =10^-9 s */
    /*  tv_usec:  us  = 10^-6 s */
    cpuTime = (startCpuTime - endCpuTime) / 1000;
    realTime = 1000000 * (startTime.tv_sec - endTime.tv_sec) +
        (startTime.tv_usec - endTime.tv_usec);
    cpuUsage = cpuTime / (double)(realTime);
 
    /* display cpuUsage by percentage */
    cpuUsage *= 100;
     
    /* make output data and exit status for nagios*/
    if (cpuUsage > critical) {
        output = "CRITICAL";
        ret    = CRITICAL;
    } else if (cpuUsage > warning){
        output = "WARNING";
        ret    = WARNING;
    } else {
        output = "OK";
        ret    = OK;
    }
    printf("%s CPU:%.2f%%|CPU=%.2f\n",output,cpuUsage,cpuUsage);
 
    return ret;
}
