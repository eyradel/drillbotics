/*
Date: May 2022
@authors: DrillMeta [D.E Braimah, Joel Mensah, Oswald Owusu, and Prince Mensah]
Program Description: 
The RSS (Rotary Steerable System) is one of the modern technologies used
for bit steering in directional well drilling. It applies the push-the-bit
technique [1]. The advantage it has over the previous down-hole motor
technologies is that it does not need to be stopped when the tool face is
facing the desired direction. It can create potential problems like pipe
sticking or packoff of tools, since the cuttings are not being rotated and
could create a bed of cuttings easier [2]. The tool accomplishes the tasks
varying from simple gravity-based to more complex internal driveshafts of
the BHA by the application of side forces from pads against the borehole
wall. Some RSSs also employ automatic drilling modes where a well path is
automatically steered using a programmed closed-loop control system [3]
[4].
*/
#ifndef RSSEQUIPMENT_H
#define RSSEQUIPMENT_h

/*Header files*/
#include <string>


class RSSEquipment
{
    public:
    /*Constant Inputs*/

    /*Set the elastic Modulus of the system*/
    void setElasticModulus(double _elasticModulus);

    /*Set the actuator to Bit distance*/
    void setActuatorToBitDistance(double _actuatorToBit);

    /*Set the actuator to stabilizer distance*/
    void setActuatorToStabilizer(double _actuatorToStabilizer);

    /*Set the outeside diameter of the RSS tool, OD*/
    void setOutsideDiameterRSS(double _outsideDiameterRSS);

    /*set the Internal diamter of the RSS tool, ID*/
    void setInternalDiameterRSS(double _insideDiameterRSS);

    /*set the maximum offset of the RSS tool*/
    void setMaximumOffsetRSS(double _maxOffset);

    /*set the maximum degree tolerance of the tool*/
    void setMaximumDegreeTolerance(double _maxDegreeTolerance);

    /*Set the Sliding Coefficient*/
    void setSlidingCoefficient(double _slidingCoefficient);

    /*Constant Outputs*/

    /*Get the Elastic Modulus*/
    double getElasticModulus() const;

    /*Get the actuator to bit distance*/
    double getActuatorToBitDistance() const;

    /*Get the actuator to stabilizer distance*/
    double getActuatorToStabilizer() const;

    /*Get the outer diameter of the RSS tool */
    double getOuterDiameterRSS() const;

    /*Get the  Inner diamter of the RSS tool */
    double getInnerDiameterRSS() const;

    /*Get the maximum offset of the RSS tool*/
    double getMaximumOffsetRSS() const;

    /*Get the Maximum Degree of tolerance*/
    double getMaximumDegreeTolerance() const;

    /*Get the sliding coeffecient*/
    double getSlidingCoefficient() const;

    /*Variable Inputs*/

    /*Copy in the Inclination Values from the well design file*/
    void copyInInclinationData(double _inclination[]);

    /*Copy in the TVD at the Bit for the target survey station*/
    void copyInTrueVerticalDepth(double _trueVerticalDepth[]);

    /*Copy in the Horizontal Displacement at the next survey station*/
    void copyInHorizontalDisplacement(double _horizontalDisplacement[]);

    /*Variable Outputs*/

    /*Copy out the natural displacement*/
    void copyOuttheNaturalDisplacement(double _naturalDisplacement[]) const;

    /*Copy out the offset displacement*/
    void copyOuttheOffsetDisplacement(double _offsetDisplacement[]) const;

    /*Copy out the force due to the natural displacement*/ 
    void copyOuttheForceNaturalDisplacement(double _forceNaturalDisplacement[]) const;

    /*Copy out the force due to the offset displacement*/
    void copyOuttheForceOffsetDisplacement(double _forceOffsetDisplacement[]) const;

    /*Copy the force on the bit*/
    void copyOuttheForceOnBit(double _forceOnBit[]) const;

    /*output the natural displacement at a particular SSI*/
    double getNaturalDisplacementSSI(int _location) const;

    /*Output the offset displacement at a particular SSI*/
    double getOffsetDisplacementSSI(int _location) const;

    /*Output the force at natural displacement at a particular SSI*/
    double getForceNaturalDisplacementSSI(int _location) const;

    /*Output the force at offset displacement at a particular SSI*/
    double getForceOffsetDisplacementSSI(int _location) const;

    /*Output the force on the bit at a particular SSI*/
    double getForceBitSSI(int _location) const;

    /*File tranfer functions*/
    void executeFileTransferRSSequipment(std::string _fileName, std::string &_errorMessage, std::string _teamName);

    /*Constructors and Destructors*/
    RSSEquipment(double _constantValuesRSS[], double _inclinationData[], double _trueVerticalDepthData[], double _horizontalDisplacementData[], double _tvdKickOffPoint, double _radiusofCurvature, int _dataSize);
    ~RSSEquipment();
    
    private: 

    /*Computational Variables*/

    /*Constants*/
    double elasticModulus; // elastic Modulus of the material |
    double actuatorToBit; //acutator to bit, should be in feet
    double actuatorToStabilizer; //actuator to Stabilizer, should be in fee
    double outsideDiameter; //outside diameter of the RSS tool
    double insideDiameter; // Inside diamter of the RSS tool
    double maximumOffset; // the maximum offset of the RSS tool
    double maximumDegreeTolerance;// the maximum degree of the tolerance
    double slidingCoefficient; // the sliding coefficient for compensation for slides.
/*---------------------------------------------------------------------------------------------*/
    /* Outputs Array parameters*/
    double *naturalDisplacement; // natural displacement
    double *offsetDisplacement; //offset displacement
    double *forceNaturalDisplacement;//natural displacement
    double *forceOffsetDisplacement; //offset dispalcement
    double *forceOnBit; // force on bit

    /*Other vital variables*/
    double trueVerticalDepthKOP;
    double radiusOfCurvature;
    int surveyDataSize;

    /*Inputs Array parameters*/
    double *inclinationData;
    double *trueVerticalDepthData;
    double *horizontalDisplacemenData;
   
    /*Computational functions*/
    double calculateMomentofInertia() const;
    double calculateTotalLength() const;
    double calculateForceNaturalDisplacement(int _location);
    double calculateForceOffsetDisplacement(int _location);
    double calculateArcLength(int _location) const;
    void   calculateNaturalDisplacement(int _location);
    void   calculateOffsetDisplacement(int _location);
    void   calculateForceOnBit(int _location);
    
    /*execution function*/
    void executeBitForceCalculations(int _location);
    void executeFileTransfer();

    /*Convertion functions*/
    double convertToFeet(double _meters);
    int convertToFeet(int _meters);

    double convertToMeters(double _feet);
    int convertToMeters(int _feet);
};
#endif

#ifndef RSSEXECUTION_H
#define RSSEXECUTION_H
class RSSExecution
{
    public:
    /*Inputs functions*/

    /*Function to get the time steps*/
    void setTimeSteps(int _timeSteps); 

    /*Get the axial rate of penetration at a particular survey station*/
    void setAxialRateOfPenetrationSSI(int _location, double _ropAxial);

    /*Get the Normal Rate of Penetration*/
    void setNormalRateOfPenetrationSSI(int _location, double _ropNormal);

    /*Copy In the axial Rate of Penetration*/
    void copyInAxialRateOfPenetration(double _axialRateOfPenetration[]);

    /*Copy In the Normal Rate of Penetration*/
    void copyInNormalOfPenetration(double _normalRateOfPenetration[]);

    /**/


    /*Outputs*/

    /*Get the inclination angle at a particular location*/
    double getInclinationSSI(int _location) const;

    /*Get the measured Depth at a particular survey station*/
    double getMeasuredDepthSSI(int _location) const;

    /*Get the true vertical depth at a particular survey station*/
    double getTrueVerticalDepthSSI(int _location) const;

    /*Get the Dog leg severity at a particular Survey Station*/
    double getDogLegSeveritySSI(int _location) const;

    /*Copy Out the normal inclination*/
    void copyOutInclination(double _inlcinationData[]) const;

    /*Copy Out the Measured Depth*/
    void copyOutMeasuredDepth(double _measuredData[]) const;

    /**Copy out the true vertical depth*/
    void copyOutTrueVeticalDepth(double _trueVerticalDepth[]) const;

    /*Copy Out the Dog Leg severity*/
    void copyOutDogSeverity(double _doglegSeverity[]) const;
      
   
    /*Essential Public functions*/
    void executeRSSExecution();

    /*File transfer functions*/
    void executeFileTransferRSSSteering(std::string _fileName, std::string &_errorMessage, std::string _teamName);

    /*Constructor and Destructor*/
    RSSExecution(double _ropAxial[], double _ropNormal[], int _dataSize, int _timeElapse );
    ~RSSExecution();
    private:

    /*Declaring the main variables*/
    
    int arrayDataSize;//array size 

    int timeElapse;

    /*Initializing the arrays*/
    double *inclinationAngle;
    double *measuredDepth;
    double *trueVerticalDepth;
    double *dogLegSeverity;
    double *ropNormal;
    double *ropAxial;
    
    /*Computational functions*/

    /*calculating the inclination*/
    double calculateInclination(int _location);

    /*Calculating the Measured Depth*/
    double calculateMeasuredDepth(int _location);

    /*Calculating the True Vertical Depth*/
    double calculateTrueVerticalDepth(int _location);

    /*Calculating the Dog leg severity*/
    double calculateDogLegSeverity(int _location);

    /*Execute RSSSteering*/
    void executRSSSteering(int _location);

    /*Vital computations*/
};

#endif