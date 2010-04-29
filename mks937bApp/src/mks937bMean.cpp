/*******************************************************************************
* mks937aMean.c
* genSub record to calculate the mean pressure from a number of IMGs
*
* Pete Owens
* 26/6/06
*/

#include <vxWorks.h>
#include <types.h>
#include <genSubRecord.h>
#include <epicsExport.h>
#include <registryFunction.h>

#define STA_OK       (0)
#define STA_OK1      (1)
#define STA_NO_GAUGE (11)
#define P_MIN        (1.99e-11)
#define P_MAX        (1.01e-3)

/*******************************************************************************
* mks937aMeanInit
* Initialisation function - Does nothing
*/
long mks937aMeanInit (struct genSubRecord *psub)
{
    return 0;
}

/*******************************************************************************
* mks937aMeanCalc
* calculate the mean pressure from up to IMGs
* Only include IMGs where the status is OK (0 or 1)
*
* Inputs:
* INPA - number of IMGs
* INPB...INPK - IMG pressure
* INPL...INPU - IMG status
*
* Outputs:
* VALA - Mean Pressure
* VALB - Archive deadband (VALB/20)
* VALB - Status (0 = OK, 1 = OK but some gauges poor, 11 = no gauges)
*
* Return: number of contributing gauges
*/
long mks937aMeanCalc (struct genSubRecord *psub)
{
    long   n        = 0;            /* counter                                */
    long   status   = STA_NO_GAUGE; /* output status       (output -> VALA)   */
    long   nImgs    = 0;            /* number of IMGs      (input  <- INPA)   */
    long   nGood    = 0;            /* number of good IMGs (return value)     */ 
    double sum      = 0.0;          /* sum of IMG pressures                   */
    double mean     = 0.0;          /* mean pressure       (output -> VALB)   */
    double pmax     = P_MIN;        /* maximum pressure    (output -> VALC)   */
    double pmin     = P_MAX;        /* mimimum pressure    (output -> VALD)   */
    double deadband = 0.0;          /* archive deadband    (output -> VALB)   */
    double p[10];                   /* input pressure      (input  <- INPB-K) */
    double s[10];                   /* input status        (input  <- INPL-U) */

    /*
    * Extract inputs
    */
    nImgs = *(long *)   psub->a;
    p[0]  = *(double *) psub->b;
    p[1]  = *(double *) psub->c;
    p[2]  = *(double *) psub->d;
    p[3]  = *(double *) psub->e;
    p[4]  = *(double *) psub->f;
    p[5]  = *(double *) psub->g;
    p[6]  = *(double *) psub->h;
    p[7]  = *(double *) psub->i;
    p[8]  = *(double *) psub->j;
    p[9]  = *(double *) psub->k;
    s[0]  = *(long *)   psub->l;
    s[1]  = *(long *)   psub->m;
    s[2]  = *(long *)   psub->n;
    s[3]  = *(long *)   psub->o;
    s[4]  = *(long *)   psub->p;
    s[5]  = *(long *)   psub->q;
    s[6]  = *(long *)   psub->r;
    s[7]  = *(long *)   psub->s;
    s[8]  = *(long *)   psub->t;
    s[9]  = *(long *)   psub->u;

    /*
    * Calculate mean
    */
    for (n = 0, nGood = 0, sum = 0; n < nImgs; n++)
    {
        if ((s[n] == STA_OK || s[n] == STA_OK1) && p[n] >= P_MIN && p[n] <= P_MAX)
        {
            sum += p[n];
            nGood++;
            pmax = (p[n] > pmax) ? p[n] : pmax;
            pmin = (p[n] < pmin) ? p[n] : pmin;
        }
    }

    if (nGood > 0)
    {
        mean = sum / (double) nGood;
        deadband = mean / 20.0; 
        status = (nGood == nImgs) ? STA_OK : STA_OK1;
    }

    /*
    * Set outputs
    */
    *(long *)   psub->vala = status;
    *(double *) psub->valb = mean; 
    *(double *) psub->valc = pmax; 
    *(double *) psub->vald = pmin; 

    return nGood;
}
/*******************************************************************************
*/

/* Only register functions in R3.14 */
#ifdef EPICS_R3_14
epicsRegisterFunction(mks937aMeanInit);
epicsRegisterFunction(mks937aMeanCalc);
#endif

