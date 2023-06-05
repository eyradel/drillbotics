/*
 Project details
*/

/*Included libraries*/
#include <cmath>
#include <string>
#include "RSSEquipment.h"
#include <fstream>

/*Global Constant*/
const double PI = 3.14159265358979323846;
const std::string fileExtension= ".csv";

/*Constant Inputs*/
void RSSEquipment::setElasticModulus(double _elasticModulus)
{
    elasticModulus = _elasticModulus;
}
void RSSEquipment::setActuatorToBitDistance(double _actuatorToBit)
{
    actuatorToBit = _actuatorToBit;
}
void RSSEquipment::setActuatorToStabilizer(double _actuatorToStabilizer)
{
    actuatorToStabilizer = _actuatorToStabilizer;
}
void RSSEquipment::setOutsideDiameterRSS(double _outsideDiameterRSS)
{
    outsideDiameter = _outsideDiameterRSS;
}
void RSSEquipment::setInternalDiameterRSS(double _insideDiameterRSS)
{
    insideDiameter = _insideDiameterRSS;
}
void RSSEquipment::setMaximumOffsetRSS(double _maxOffset)
{
    maximumOffset = _maxOffset;
}
void RSSEquipment::setMaximumDegreeTolerance(double _maxDegreeTolerance)
{
    maximumDegreeTolerance = _maxDegreeTolerance;
}
void RSSEquipment::setSlidingCoefficient(double _slidingCoefficient)
{
    slidingCoefficient = _slidingCoefficient;
}

/*Constant Outputs*/
double RSSEquipment::getElasticModulus() const
{
    return elasticModulus;
}
double RSSEquipment::getActuatorToBitDistance() const
{
    return actuatorToBit;
}
double RSSEquipment::getActuatorToStabilizer() const
{
    return actuatorToStabilizer;
}
double RSSEquipment::getOuterDiameterRSS() const
{
    return outsideDiameter;
}
double RSSEquipment::getInnerDiameterRSS() const
{
    return insideDiameter;
}
double RSSEquipment::getMaximumOffsetRSS() const
{
    return maximumOffset;
}
double RSSEquipment::getMaximumDegreeTolerance() const
{
    return maximumDegreeTolerance;
}
double RSSEquipment::getSlidingCoefficient() const
{
    return slidingCoefficient;
}

/*Variables Inputs*/
void RSSEquipment::copyInInclinationData(double _inclination[])
{
    for (int _i_ = 0; _i_ <= surveyDataSize; _i_++)
    {
        inclinationData[_i_] = _inclination[_i_];
    }
}
void RSSEquipment::copyInTrueVerticalDepth(double _trueVerticalDepth[])
{
    for (int _i_ = 0; _i_ <= surveyDataSize; _i_++)
    {
        trueVerticalDepthData[_i_] = _trueVerticalDepth[_i_];
    }
}
void RSSEquipment::copyInHorizontalDisplacement(double _horizontalDisplacement[])
{
    for (int _i_ = 0; _i_ <= surveyDataSize; _i_++)
    {
        horizontalDisplacemenData[_i_] = _horizontalDisplacement[_i_];
    }
}

/*Variable Outputs*/
void RSSEquipment::copyOuttheNaturalDisplacement(double _naturalDisplacement[]) const
{
    for (int _i_ = 0; _i_ <= surveyDataSize; _i_++)
    {
        _naturalDisplacement[_i_] = naturalDisplacement[_i_];
    }
}
void RSSEquipment::copyOuttheOffsetDisplacement(double _offsetDisplacement[]) const
{
    for (int _i_ = 0; _i_ <= surveyDataSize; _i_++)
    {
        _offsetDisplacement[_i_] = offsetDisplacement[_i_];
    }
}
void RSSEquipment::copyOuttheForceNaturalDisplacement(double _forceNaturalDisplacement[]) const
{
    for (int _i_ = 0; _i_ <= surveyDataSize; _i_++)
    {
        _forceNaturalDisplacement[_i_] = forceNaturalDisplacement[_i_];
    }
}
void RSSEquipment::copyOuttheForceOffsetDisplacement(double _forceOffsetDisplacement[]) const
{
    for (int _i_ = 0; _i_ <= surveyDataSize; _i_++)
    {
        _forceOffsetDisplacement[_i_] = forceOffsetDisplacement[_i_];
    }
}
void RSSEquipment::copyOuttheForceOnBit(double _forceOnBit[]) const
{
    for (int _i_ = 0; _i_ <= surveyDataSize; _i_++)
    {
        _forceOnBit[_i_] = forceOnBit[_i_];
    }
}

/*Get data at various SSI*/
double RSSEquipment::getNaturalDisplacementSSI(int _location) const
{
    return naturalDisplacement[_location];
}
double RSSEquipment::getOffsetDisplacementSSI(int _locaiton) const
{
    return offsetDisplacement[_locaiton];
}
double RSSEquipment::getForceNaturalDisplacementSSI(int _location) const
{
    return forceNaturalDisplacement[_location];
}
double RSSEquipment::getForceOffsetDisplacementSSI(int _location) const
{
    return forceOffsetDisplacement[_location];
}
double RSSEquipment::getForceBitSSI(int _location) const
{
    return forceOnBit[_location];
}

double RSSEquipment::calculateMomentofInertia() const
{
    return ((PI / 64) * ((pow(outsideDiameter, 4)) - (pow(insideDiameter, 4))));
}
double RSSEquipment::calculateTotalLength() const
{
    return actuatorToBit + actuatorToStabilizer;
}
double RSSEquipment::calculateForceNaturalDisplacement(int _location)
{
    return ((3 * naturalDisplacement[_location] * elasticModulus * calculateMomentofInertia()) / ((pow(actuatorToBit, 2)) * actuatorToStabilizer));
}
double RSSEquipment::calculateForceOffsetDisplacement(int _location)
{
    return ((3 * offsetDisplacement[_location] * elasticModulus * calculateMomentofInertia()) / ((pow(actuatorToBit, 2)) * actuatorToStabilizer));
}
double RSSEquipment::calculateArcLength(int _location) const
{
    return (inclinationData[_location] / 360) * (2 * PI * radiusOfCurvature);
}
void RSSEquipment::calculateNaturalDisplacement(int _location)
{
    if (trueVerticalDepthData[_location] <= trueVerticalDepthKOP)
    {
        naturalDisplacement[_location] = 0;
    }
    else
    {
        if (calculateArcLength(_location) < actuatorToBit)
        {
            // finding the chord length from the actuator to Bit
            double _AI_ = std::abs(trueVerticalDepthData[_location] - (trueVerticalDepthKOP - actuatorToBit + calculateArcLength(_location))); // vertical
            double _IB_ = horizontalDisplacemenData[_location];
            double _Aprime_ = sqrt((pow(_AI_, 2)) + (pow(_IB_, 2)));
            double _SI_ = std::abs(trueVerticalDepthData[_location] - (trueVerticalDepthKOP - calculateTotalLength() + calculateArcLength(_location))); // vertical
            // double _Sprime_ = sqrt((pow(_SI_,2))+(pow(_IB_,2)));
            double _gAngle_ = atan(_SI_ / _IB_);

            // superimposing session
            double _BBprime_ = _Aprime_ * cos(_gAngle_); // horizontal
            double _BprimeL_ = _Aprime_ * sin(_gAngle_); // vertical

            // Coordinates at point L
            double _tvdAtL_ = trueVerticalDepthData[_location] - _BprimeL_;
            double _hdAtL_ = horizontalDisplacemenData[_location] - _BBprime_;

            // coordinates at point A
            double _tvdAtA_ = (trueVerticalDepthKOP - calculateTotalLength() + calculateArcLength(_location));

            // Natural Displacement
            naturalDisplacement[_location] = convertToMeters(sqrt((pow(_hdAtL_, 2)) + (pow((_tvdAtL_ - _tvdAtA_), 2))));
        }
        else if (calculateArcLength(_location) == actuatorToBit)
        {
            double _AI_ = std::abs(trueVerticalDepthData[_location] - (trueVerticalDepthKOP)); // vertical
            double _IB_ = horizontalDisplacemenData[_location];
            double _Aprime_ = sqrt((pow(_AI_, 2)) + (pow(_IB_, 2)));
            double _SI_ = std::abs(trueVerticalDepthData[_location] - trueVerticalDepthKOP + calculateTotalLength());
            double _gAngle_ = atan(_SI_ / _IB_);

            // superimposing session
            double _BBprime_ = _Aprime_ * cos(_gAngle_); // horizontal
            double _BprimeL_ = _Aprime_ * sin(_gAngle_); // vertical

            // Coordinates at point L
            double _tvdAtL_ = trueVerticalDepthData[_location] - _BprimeL_;
            double _hdAtL_ = horizontalDisplacemenData[_location] - _BBprime_;

            // coordinates at point A
            double _tvdAtA_ = (trueVerticalDepthKOP);

            // Natural Displacement
            naturalDisplacement[_location] = convertToMeters(sqrt((pow(_hdAtL_, 2)) + (pow((_tvdAtL_ - _tvdAtA_), 2))));
        }
        else if (actuatorToBit < calculateArcLength(_location) && calculateTotalLength() > calculateArcLength(_location))
        {
            // At the stabilizer point
            double _SI_ = std::abs(trueVerticalDepthData[_location] - trueVerticalDepthKOP + calculateTotalLength() - calculateArcLength(_location));
            double _IB_ = horizontalDisplacemenData[_location];
            double _gAngle_ = atan(_SI_ / _IB_);

            // At the actuator pointer
            double _thetaAtAI_ = 28.64788976 * actuatorToBit;
            double _delta_ = inclinationData[_location] - _thetaAtAI_;

            double _AI_ = std::abs(trueVerticalDepthData[_location] - (trueVerticalDepthKOP + (radiusOfCurvature * sin(_delta_)))); // vertical
            double _BI_ = _IB_ - radiusOfCurvature + (radiusOfCurvature * cos(_delta_));
            double _Aprime_ = sqrt((pow(_AI_, 2)) + (pow(_BI_, 2)));

            // At the point L
            // superimposing session
            double _BBprime_ = _Aprime_ * cos(_gAngle_); // horizontal
            double _BprimeL_ = _Aprime_ * sin(_gAngle_); // vertical

            double _tvdAtL_ = trueVerticalDepthData[_location] - _BprimeL_;
            double _hdAtL_ = horizontalDisplacemenData[_location] - _BBprime_;

            // coordinates at point A
            double _tvdAtA_ = trueVerticalDepthKOP + (radiusOfCurvature * sin(_delta_));
            double _hdAtA_ = radiusOfCurvature - (radiusOfCurvature * cos(_delta_));

            // Natural Displacement
            naturalDisplacement[_location] = convertToMeters(sqrt((pow((_hdAtL_ - _hdAtA_), 2)) + (pow((_tvdAtL_ - _tvdAtA_), 2))));
        }
        else if (actuatorToBit < calculateArcLength(_location) && calculateTotalLength() == calculateArcLength(_location))
        {
            // At the stabilizer point
            double _SI_ = std::abs(trueVerticalDepthData[_location] - trueVerticalDepthKOP);
            double _IB_ = horizontalDisplacemenData[_location];
            double _gAngle_ = atan(_SI_ / _IB_);

            // At the point A
            double _thetaAtAI_ = 28.64788976 * actuatorToBit;
            double _delta_ = inclinationData[_location] - _thetaAtAI_;

            double _AI_ = std::abs(trueVerticalDepthData[_location] - ((radiusOfCurvature * sin(_delta_)))); // vertical
            double _BI_ = _IB_ - radiusOfCurvature + (radiusOfCurvature * cos(_delta_));
            double _Aprime_ = sqrt((pow(_AI_, 2)) + (pow(_BI_, 2)));

            // coordinates at point A
            double _tvdAtA_ = trueVerticalDepthKOP + (radiusOfCurvature * sin(_delta_));
            double _hdAtA_ = radiusOfCurvature - (radiusOfCurvature * cos(_delta_));

            // At the point L
            // superimposing session
            double _BBprime_ = _Aprime_ * cos(_gAngle_); // horizontal
            double _BprimeL_ = _Aprime_ * sin(_gAngle_); // vertical

            double _tvdAtL_ = trueVerticalDepthData[_location] - _BprimeL_;
            double _hdAtL_ = horizontalDisplacemenData[_location] - _BBprime_;

            // Natural Displacement
            naturalDisplacement[_location] = convertToMeters(sqrt((pow((_hdAtL_ - _hdAtA_), 2)) + (pow((_tvdAtL_ - _tvdAtA_), 2))));
        }
        else
        {
            // Analysis at the point S
            double _thetaSI_ = 28.64788976 * calculateTotalLength();
            double _thetaPrime_ = inclinationData[_location] - _thetaSI_;
            double _SI2Prime_ = trueVerticalDepthData[_location] - trueVerticalDepthKOP - (radiusOfCurvature * sin(_thetaPrime_));
            double _I2PrimeB_ = horizontalDisplacemenData[_location] - radiusOfCurvature + (radiusOfCurvature * cos(_thetaPrime_));
            double _gAngle_ = atan(_SI2Prime_ / _I2PrimeB_);

            // Analysis at the point A
            double _thetaAI_ = 28.64788976 * actuatorToBit;
            double _delta_ = inclinationData[_location] - _thetaAI_;
            double _AI_ = trueVerticalDepthData[_location] - _thetaAI_;
            double _IprimeB_ = horizontalDisplacemenData[_location] - radiusOfCurvature - (radiusOfCurvature * cos(_delta_));
            double _Aprime_ = sqrt((pow(_AI_, 2)) + (pow(_IprimeB_, 2)));

            // Coordinates at the point A
            double _tvdAtA_ = trueVerticalDepthKOP + (radiusOfCurvature * sin(_delta_));
            double _hdAtA_ = radiusOfCurvature - (radiusOfCurvature * cos(_delta_));

            // At the point L
            // superimposing session
            double _BBprime_ = _Aprime_ * cos(_gAngle_); // horizontal
            double _BprimeL_ = _Aprime_ * sin(_gAngle_); // vertical

            double _tvdAtL_ = trueVerticalDepthData[_location] - _BprimeL_;
            double _hdAtL_ = horizontalDisplacemenData[_location] - _BBprime_;

            // Natural Displacement
            naturalDisplacement[_location] = sqrt((pow((_hdAtL_ - _hdAtA_), 2)) + (pow((_tvdAtL_ - _tvdAtA_), 2)));
        }
    }
}
void RSSEquipment::calculateOffsetDisplacement(int _location)
{
    if (trueVerticalDepthData[_location] <= trueVerticalDepthKOP)
    {
        offsetDisplacement[_location] = 0;
    }
    else
    {
        if ((inclinationData[_location] - inclinationData[_location - 1]) > maximumDegreeTolerance)
        {
            offsetDisplacement[_location] = std::abs(maximumOffset);
        }
        else
        {
            offsetDisplacement[_location] = std::abs((inclinationData[_location] - inclinationData[_location - 1] * slidingCoefficient * maximumOffset));
        }
    }
}
void RSSEquipment::calculateForceOnBit(int _location)
{
    forceOnBit[_location] = forceNaturalDisplacement[_location] + forceOffsetDisplacement[_location];
}
void RSSEquipment::executeBitForceCalculations(int _location)
{
    calculateForceOffsetDisplacement(_location);
    calculateForceNaturalDisplacement(_location);
    calculateForceOnBit(_location);
}
void RSSEquipment::executeFileTransferRSSequipment(std::string _fileName, std::string &_errorMessage, std::string _teamName)
{
    std::string _fileName_ = _fileName + fileExtension;
    std::ofstream _rssToolDataCSVfile_;
    _rssToolDataCSVfile_.open(_fileName_.c_str());
    _rssToolDataCSVfile_ << "Team Name: "
                         << "," << _teamName << std::endl;
    _rssToolDataCSVfile_ << "Natural Displacement"
                         << ","
                         << "Offset Displacement"
                         << ","
                         << "Force| Natural Displacement"
                         << ","
                         << "Force| Offset  Displacement"
                         << ","
                         << "Force| On Bit" << std::endl;
    for (int _i_ = 0; _i_ <= surveyDataSize; _i_++)
    {
        executeBitForceCalculations(_i_);
        _rssToolDataCSVfile_ << naturalDisplacement[_i_] << "," << offsetDisplacement[_i_] << "," << forceNaturalDisplacement[_i_] << "," << forceOffsetDisplacement[_i_] << "," << forceOnBit[_i_] << std::endl;
    }
    _errorMessage = "Data tranfer successful";
    _rssToolDataCSVfile_.close();
}
/*Convertions*/
double RSSEquipment::convertToFeet(double _meters)
{
    return (_meters / 0.3048);
}
int RSSEquipment::convertToFeet(int _meters)
{
    return (_meters / 0.3048);
}
double RSSEquipment::convertToMeters(double _feet)
{
    return (_feet * 0.3048);
}
int RSSEquipment::convertToMeters(int _feet)
{
    return (_feet * 0.3048);
}
/*Constructor and Destructor*/
RSSEquipment::RSSEquipment(double _constantValuesRSS[], double _inclinationData[], double _trueVerticalDepthData[], double _horizontalDisplacementData[], double _tvdKickoffPoint, double _radiusOfCurvature, int _dataSize)
{
    // outputs
    naturalDisplacement = new double[_dataSize];
    offsetDisplacement = new double[_dataSize];
    forceNaturalDisplacement = new double[_dataSize];
    forceOffsetDisplacement = new double[_dataSize];
    forceOnBit = new double[_dataSize];

    // inputs
    inclinationData = new double[_dataSize];
    trueVerticalDepthData = new double[_dataSize];
    horizontalDisplacemenData = new double[_dataSize];

    // initializing
    for (int _i_ = 0; _i_ <= _dataSize; _i_++)
    {
        naturalDisplacement[_i_] = 0;
        offsetDisplacement[_i_] = 0;
        forceNaturalDisplacement[_i_] = 0;
        forceOffsetDisplacement[_i_] = 0;
        forceOnBit[_i_] = 0;
        inclinationData[_i_] = 0;
        trueVerticalDepthData[_i_] = 0;
        horizontalDisplacemenData[_i_] = 0;
    }

    // Tranferring the constant values
    _constantValuesRSS[0] = elasticModulus;
    _constantValuesRSS[1] = convertToFeet(actuatorToBit);
    _constantValuesRSS[2] = convertToFeet(actuatorToStabilizer);
    _constantValuesRSS[3] = outsideDiameter;
    _constantValuesRSS[4] = insideDiameter;
    _constantValuesRSS[5] = maximumOffset;
    _constantValuesRSS[6] = maximumDegreeTolerance;
    _constantValuesRSS[7] = slidingCoefficient;

    // other vital values
    trueVerticalDepthKOP = _tvdKickoffPoint;
    radiusOfCurvature = _radiusOfCurvature;
    surveyDataSize = _dataSize;

    // Inclination Data transfere
    copyInInclinationData(_inclinationData);

    // True Vertical Depth Data
    copyInTrueVerticalDepth(_trueVerticalDepthData);

    // horizontal Displacement Data
    copyInHorizontalDisplacement(_horizontalDisplacementData);
}
RSSEquipment::~RSSEquipment()
{
    delete[] naturalDisplacement;
    delete[] offsetDisplacement;
    delete[] forceNaturalDisplacement;
    delete[] forceOffsetDisplacement;
    delete[] forceOnBit;
    delete[] inclinationData;
    delete[] trueVerticalDepthData;
    delete[] horizontalDisplacemenData;
}

/*****************************************************************************************/
// Class RSSExecution
/*****************************************************************************************/

/*Inputs*/

void RSSExecution::setTimeSteps(int _timeStep)
{
    timeElapse = _timeStep;
}
void RSSExecution::setAxialRateOfPenetrationSSI(int _location, double _ropAxial)
{
    ropAxial[_location] = _ropAxial;
}
void RSSExecution::setNormalRateOfPenetrationSSI(int _location, double _ropNormal)
{
    ropNormal[_location] = _ropNormal;
}
void RSSExecution::copyInAxialRateOfPenetration(double _axialRateOfPenetration[])
{
    for (int _i_ = 0; _i_ <= arrayDataSize; _i_++)
    {
        ropAxial[_i_] = _axialRateOfPenetration[_i_];
    }
}
void RSSExecution::copyInNormalOfPenetration(double _normalRateOfPenetration[])
{
    for (int _i_ = 0; _i_ <= arrayDataSize; _i_++)
    {
        ropNormal[_i_] = _normalRateOfPenetration[_i_];
    }
}

/*Outputs*/
double RSSExecution::getInclinationSSI(int _location) const
{
    return inclinationAngle[_location];
}
double RSSExecution::getMeasuredDepthSSI(int _location) const
{
    return measuredDepth[_location];
}
double RSSExecution::getTrueVerticalDepthSSI(int _location) const
{
    return trueVerticalDepth[_location];
}
double RSSExecution::getDogLegSeveritySSI(int _location) const
{
    return dogLegSeverity[_location];
}
void RSSExecution::copyOutInclination(double _inclination[]) const
{
    for (int _i_ = 0; _i_ <= arrayDataSize; _i_++)
    {
        _inclination[_i_] = inclinationAngle[_i_];
    }
}
void RSSExecution::copyOutMeasuredDepth(double _measuredDepth[]) const
{
    for (int _i_ = 0; _i_ <= arrayDataSize; _i_++)
    {
        _measuredDepth[_i_] = measuredDepth[_i_];
    }
}
void RSSExecution::copyOutDogSeverity(double _dogLegSeverity[]) const
{
    for (int _i_ = 0; _i_ <= arrayDataSize; _i_++)
    {
        _dogLegSeverity[_i_] = dogLegSeverity[_i_];
    }
}
void RSSExecution::executeRSSExecution()
{
    for (int _i_ = 0; _i_ <= arrayDataSize; _i_++)
    {
        inclinationAngle[_i_] = calculateInclination(_i_);
        measuredDepth[_i_] = calculateMeasuredDepth(_i_);
        trueVerticalDepth[_i_] = calculateTrueVerticalDepth(_i_);
        dogLegSeverity[_i_] = calculateDogLegSeverity(_i_);
    }
}
double RSSExecution::calculateInclination(int _location)
{
    return (atan((ropNormal[_location]) / (ropAxial[_location])) * timeElapse);
}
double RSSExecution::calculateMeasuredDepth(int _location)
{
    double _a_ = pow(ropNormal[_location], 2);
    double _b_ = pow(ropAxial[_location], 2);
    return (sqrt(_a_ + _b_) * timeElapse);
}
double RSSExecution::calculateTrueVerticalDepth(int _location)
{
    if (_location == 0)
    {
        double _theta_ = 0 + calculateInclination(_location);
        return (calculateMeasuredDepth(_location) * cos(_theta_) * timeElapse);
    }
    else
    {
        double _theta_ = calculateInclination(_location - 1) + calculateInclination(_location);
        return (calculateMeasuredDepth(_location) * cos(_theta_) * timeElapse);
    }
}
double RSSExecution::calculateDogLegSeverity(int _location)
{
    return ((180 * calculateInclination(_location)) / (PI * calculateMeasuredDepth(_location)));
}
void RSSExecution::executeFileTransferRSSSteering(std::string _fileName, std::string &_errorMessage, std::string _teamName)
{
    std::string _fileName_ = _fileName + fileExtension;
    std::ofstream _rssSteeringDataFIle_;
    _rssSteeringDataFIle_.open(_fileName_.c_str());
    executeRSSExecution();
    _rssSteeringDataFIle_ << "Team: "
                          << "," << _teamName << std::endl;
    _rssSteeringDataFIle_ << "TVD"
                          << ","
                          << "MD"
                          << ","
                          << "Inclination"
                          << ","
                          << "Dog Leg Severity"
                          << ","
                          << "ROP Normal"
                          << ","
                          << "ROP Axial" << std::endl;
    for (int _i_ = 0; _i_ <= arrayDataSize; _i_++)
    {
        _rssSteeringDataFIle_ << trueVerticalDepth[_i_] << "," << measuredDepth[_i_] << "," << inclinationAngle[_i_] << "," << dogLegSeverity[_i_] << "," << ropNormal[_i_] << "," << ropAxial[_i_] << std::endl;
    }

    _rssSteeringDataFIle_.close();
}

RSSExecution::RSSExecution(double _ropAxial[], double _ropNormal[], int _dataSize, int _timeElapse)
{
    // Creating the arrays
    inclinationAngle = new double[_dataSize];
    measuredDepth = new double[_dataSize];
    trueVerticalDepth = new double[_dataSize];
    dogLegSeverity = new double[_dataSize];
    ropAxial = new double[_dataSize];
    ropNormal = new double[_dataSize];

    // initializing the values
    for (int _i_ = 0; _i_ <= _dataSize; _i_++)
    {
        inclinationAngle[_i_] = 0;
        measuredDepth[_i_] = 0;
        trueVerticalDepth[_i_] = 0;
        dogLegSeverity[_i_] = 0;
        ropAxial[_i_] = 0;
        ropNormal[_i_] = 0;
    }

    timeElapse = _timeElapse;
    arrayDataSize = _dataSize;
    copyInNormalOfPenetration(_ropNormal);
    copyInAxialRateOfPenetration(_ropAxial);
}
RSSExecution::~RSSExecution()
{
    delete[] inclinationAngle;
    delete[] measuredDepth;
    delete[] trueVerticalDepth;
    delete[] dogLegSeverity;
    delete[] ropAxial;
    delete[] ropNormal;
}
