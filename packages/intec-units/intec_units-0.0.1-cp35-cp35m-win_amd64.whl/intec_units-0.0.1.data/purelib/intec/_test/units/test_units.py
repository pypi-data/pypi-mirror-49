import sys, math
from intec.units import *

class ShouldThrowError(RuntimeError):
    pass
    
class should_throw(object):
    def __init__(self, exc_type, err_string = None):
        self.exc_type = exc_type
        self.err_string = err_string
    def __enter__(self):
        pass
    def __exit__(self, type, value, traceback):
        if type == self.exc_type:
            if self.err_string:
                if not self.err_string in str(value):
                    raise ShouldThrowError( "Could not find %r in %r"%(self.err_string, str(value)) )
            return 1
        raise ShouldThrowError( "Should have thrown %s"%self.exc_type.__name__)


def test():    
    
    assert (1*KILOMETER+1*METER).value == 1.001
    assert (1*KILOMETER+1*METER).unit is KILOMETER
    assert (1*METER+1*KILOMETER).value == 1001
    assert (1*CENTIMETER+1*KILOMETER).unit == CENTIMETER
    
    with should_throw( TypeError, "Cannot convert unit [A] to unit [km]"):
        1*KILOMETER+1*AMPERE
    
    q = 2*KILOMETER/SECOND
    assert type(q) is VelocityQuantity
        
    q = 5*HERTZ    
    q2 = 1/q
    assert q2.unit.dims == SECOND.dims
    
    with should_throw(TypeError):
        NEWTON + METER    
    with should_throw(TypeError):
        1 + METER
    with should_throw(TypeError):
        METER + 1
    with should_throw(TypeError):
        METER + 'a'
    #with should_throw(TypeError):
    #    METER + np.zeros( (8,) )
    #with should_throw(TypeError):
    #    np.zeros( (8,) ) + METER
    with should_throw(TypeError):
        []*5*NEWTON
    with should_throw(TypeError):
        5*NEWTON*[]
   
    assert (5*NEWTON).unit is NEWTON
    
    assert 5*5*NEWTON == 25*NEWTON    
    assert 5*(5*NEWTON) == 25*NEWTON
    assert 5*NEWTON*5 == 25*NEWTON
    assert NEWTON*5*5 == 25*NEWTON
        
    assert 5*(NEWTON*METER) > 4*NEWTON*METER 
    assert NEWTON*5*METER > 4*NEWTON*METER 
    assert NEWTON*METER*5 > 4*NEWTON*METER 
    assert KILOMETER*NEWTON*5 > 4*NEWTON*METER 
    
    assert type( 5*GRAM*CENTIMETER/SECOND**2 ) is ForceQuantity
    
    ZoinkQuantity = new_Quantity( METER**10/SECOND**7, 'zoink' )
    assert type(7*METER**10/SECOND**7) is ZoinkQuantity
    
    assert KILOMETER >= KILOMETER
    assert KILOMETER > 1e5*MICROMETER
    with should_throw( TypeError, "Cannot convert unit [km] to unit [A]"):
        KILOMETER < AMPERE
    
    t1 = 3*CELCIUS
    t2 = 100*KELVIN
    assert t1 > t2
    assert t2 < t1
    assert t2.near(-173.15*CELCIUS)
        
    q = Quantity(10, CENTIMETER)
    assert type(q) is LengthQuantity
    #q = TemperatureQuantity(10, CENTIMETER)
    #assert type(q) is TemperatureQuantity
        
    q0 = 5*PERCENT
    q1 = 10*CENTIMETER
    q2 = 1.3*METER
    q3 = 3*AMPERE
    
    assert q0 == 0.05
    
    PERMIL = new_Unit( DimensionlessQuantity, 1e-3, "per mil", "per mil")
    assert 1*PERMIL == 0.001
    assert q0 > 5*PERMIL
    
    with should_throw( TypeError, "Cannot convert unit [cm] to unit [A]"):
        q1 > AMPERE
    with should_throw( TypeError, "Cannot convert unit [cm] to dimensionless number"):
        10 != q1
    with should_throw( TypeError, "Cannot convert unit [cm] to dimensionless number"):
        q1 < 10
    assert MILLIMETER < q2
    assert q1 > MILLIMETER
    assert q1 <= q2
    with should_throw(TypeError, "Cannot convert"):
        q1 != q3
    

    q = 10*CENTIMETER
    
    assert q > CENTIMETER    
    assert q >= CENTIMETER    
    assert q != CENTIMETER    
    assert q == 0.1*METER
    assert q < KILOMETER
    assert q <= KILOMETER
    assert q > 9.99*CENTIMETER
    assert q > 1*MILLIMETER
    assert q >= 8*CENTIMETER
    assert q >= 1*MILLIMETER
    assert q < 2*LIGHTYEAR
    assert q < 1*METER
    assert q <= 2*LIGHTYEAR
    assert q <= 1*METER
    assert q == .10*METER
    assert q == 10*CENTIMETER
    assert q == 100*MILLIMETER
    assert q >= 10*CENTIMETER
    assert q >= 100*MILLIMETER
    assert q <= 10*CENTIMETER
    assert q <= 100*MILLIMETER
    
    assert type(KILOWATT/MILLIWATT) == float    
    q = 2/KILOMETER
    assert str(q) == "2. 1/km"
    
    assert KILOWATT/MILLIWATT == 1e6
    assert MILLIWATT/KILOWATT == 1e-6
    #q2 = q * MILLIMETER
    #assert q2 == 0.000002
    
    rc = sys.getrefcount(MILLIWATT/KILOWATT)
    assert rc == sys.getrefcount(MILLIWATT/KILOWATT)
    assert rc == sys.getrefcount(MILLIWATT/KILOWATT)
    assert rc == sys.getrefcount(MILLIWATT/KILOWATT)
    
    q = 2/PERCENT
    assert q == 200
    
    assert MILLIAMPERE/MILLIAMPERE == 1
    q = KILOMETER/2
    assert q.unit is KILOMETER
    assert float(q.to(METER))==500
    
    with should_throw( TypeError, "Cannot multiply non-linear unit [dBm] with other unit"):
        DBM*METER
    with should_throw( TypeError, "Cannot multiply non-linear unit [C] with other unit"):
        METER*CELCIUS
    
    q = 5*SECOND**-1
    assert q.unit.qtype is FrequencyQuantity
        
    q2 = q*20
    #assert str( q2 ) == "100.000 s^-1"
    print(q2)
    assert str( q2 ) == "100. s^-1"

    q2 = 2*MINUTE
    q3 = q*q2
    assert q3 == 600
    
    q = HERTZ*HOUR
    assert q == 3600
    assert q is HERTZ*HOUR    
    
    u = PERCENT*PERCENT
    assert u == 0.0001
    assert u == PERCENT*PERCENT
    q = 5*PERCENT
    q *= 5
    assert q.unit is PERCENT
    assert q.value == 25

        
    AU = new_Unit( METER, 149597870700, "AU", "astronomical unit" )
    assert AU.factor == 149597870700
    assert AU.qtype is LengthQuantity
    q = (5*AU).to(KILOMETER)
    
    f = 1/math.tan( math.radians(1.0/3600) )    
    PARSEC = new_Unit( AU, f, "Pc", "parsec")
    assert (1*PARSEC).near( 3.26*LIGHTYEAR, .01 )
    assert not (1*PARSEC).near( 3.26*LIGHTYEAR, .001 )
    q = PARSEC.to(LIGHTYEAR)
    assert q.unit is LIGHTYEAR
    assert int(q.value) == 3
    
    assert METER.dims == (0,1,0,0,0,0,0)
    u = METER**2
    assert u.dims == (0,2,0,0,0,0,0)
    assert u is METER**2
    assert str(u) == "m^2"
    u = u**2
    assert str(u) == "(m^2)^2"
    assert u.dims == (0,4,0,0,0,0,0)
    u = u**8
    assert u.dims == (0,32,0,0,0,0,0)
    with should_throw( OverflowError, "Dimension of unit 'meter': 256"):
        u = u**8
    u = METER*METER
    assert u.dims == (0,2,0,0,0,0,0)
    
    assert ATTOMETER.name == 'attometer'
    assert ATTOMETER.symbol == 'am'
    assert ATTOMETER.factor == 1e-18

    q1 = 1008e+17*ATTOMETER
    assert q1.near( 100.8*METER )
    assert q1.to(METER).near( 100.8*METER )
    assert not (100.008*METER).near(100.007*METER)
    
    q1 = 0*DBM
    q2 = q1.to(WATT)
    assert q2.value == 0.001
    assert q2.unit is WATT
    q2 = q1.to(MILLIWATT)
    assert q2.value == 1

    q2 = 30*DBM
    q3 = q2.to(WATT)
    assert q3.value == 1
    
       
    SQUARE_YARD = YARD*YARD
    assert YARD*YARD is SQUARE_YARD
    assert SQUARE_YARD.symbol == 'yd.yd'
    assert SQUARE_YARD.qtype is AreaQuantity
    
    q1 = 5 * SQUARE_YARD
    assert q1.unit is YARD*YARD
    q1 = 5 * q1
    assert q1.unit is YARD*YARD
    assert q1.value == 25
    
    assert q1.to(SQUARE_YARD) is q1
    assert q1.to(YARD*YARD) is q1
    with should_throw(TypeError, "Cannot convert"):
        q1.to(POUND)
    q2 = q1.to(METER*METER)
    assert type(q2) is AreaQuantity
    assert q2.value == 20.903184
        
    with should_throw(TypeError, "must be Unit, not str"):
        q1 = Quantity(10.0, "kelvin")
    with should_throw(TypeError, "function takes exactly 2 arguments"):
        q1 = Quantity(10.0, KELVIN, 1)        
    q1 = Quantity(5.0, KELVIN)
    assert q1.value == 5.0
    assert q1.unit is KELVIN
    assert float(q1) == 5.0
    
    with should_throw(AttributeError, "attribute 'value' of 'Quantity' objects is not writable"):
        q1.value = 3
    with should_throw(AttributeError, "attribute 'unit' of 'Quantity' objects is not writable"):
        q1.unit = KELVIN
    
    q1 = -3*KELVIN
    assert q1.value == -3.0
    assert q1.unit is KELVIN
    
    q1 = POUND*3
    assert q1.value == 3.0
    assert q1.unit is POUND

    b = 5555555555566666666666665555555555555555555555555555555555555555555555555555555555555555
    q1 = b*KELVIN
    assert type(q1) == TemperatureQuantity
    assert q1.value == float(b)
    assert q1.unit is KELVIN
    
    q1 = POUND*.035
    assert type(q1) == MassQuantity
    assert q1.value == .035
    assert q1.unit is POUND    
    n1 = sys.getrefcount(POUND)
    q2 = q1 + 5*POUND
    assert -q2.value == -5.035
    assert q2.unit is POUND    
    assert sys.getrefcount(POUND) == n1+1
    del q2
    assert sys.getrefcount(POUND) == n1
    
    assert (5*5*KELVIN*5*5).value == 625
   
    with should_throw( OverflowError, "int too large to convert to float"):    
        300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000*q1

        
    with should_throw(TypeError):
        1/SECOND > 2*SECOND
    
    assert (1550*NANOMETER).to_frequency() > 193.41 * TERAHERTZ
    assert (1550*NANOMETER).to_frequency() < 193.42 * TERAHERTZ
    assert (1550*NANOMETER).to_frequency(HERTZ) > 193.41 * TERAHERTZ
    
    assert 5*NEWTON*METER*KILOMETER*3 == 5*NEWTON*(METER*KILOMETER)*3
    assert (5*METER)*(5*METER) == 25 * METER**2
    assert METER*5 == 2.5*METER*2
    assert METER*(5*NEWTON) == JOULE*5
    assert 1*METER*5*NEWTON == 1*(METER*5*NEWTON)
    assert 1*METER*(5*NEWTON) == 5*JOULE
    
    with should_throw(TypeError):
        1*METER == 1*JOULE    
    with should_throw(TypeError):
        DBM*SECOND        
    with should_throw(TypeError):
        (5*SECOND)*DBM    
    with should_throw(TypeError):
        (5*DBM)*SECOND
    with should_throw(TypeError):
        SECOND*(5*DBM)
    with should_throw(TypeError):
        DBM*(5*SECOND)
    with should_throw(TypeError):
        SECOND*DBM
    
    q1 = 5*KILOMETER 
    q2 = q1.to(METER)
    assert q1 == q2
    assert q2.unit == METER
    assert q2.value == 5000
    assert str((5*GRAM).to(KILOGRAM)) == '0.005 kg'
    assert (10*DBM).to(WATT) == 10*DBM
    assert (10*DBM).to(DBM).value == 10 
        
    with should_throw(TypeError):
        5 == 3*PICOMETER
    with should_throw(TypeError):
        (10*WATT).to(DBM) == 10
    assert (0*CELCIUS).to(KELVIN).value == 273.15
    assert str( (0*KELVIN).to(CELCIUS) ) ==  "-273.150 C"
    with should_throw(TypeError, "Cannot convert"):
        (5*GRAM).to(NEWTON)

    assert 5*NEWTON + 7*NEWTON == 12*NEWTON
    assert 1*KILOMETER + 1*METER > 1000 * METER
    with should_throw(TypeError, "Cannot convert"):
        1*METER + 1*NEWTON
        
    assert 1*JOULE + 1*NEWTON*METER == WATT*2*SECOND    
    assert 1*METER/SECOND * HOUR == 3.6*KILOMETER
    assert 1 == 1*WATT*SECOND / (1*NEWTON*METER)
    assert 1/SECOND*HOUR == 3600
    q1 = 1*HERTZ
    q2 = 1/SECOND
    q3 = 1*SECOND**-1
    assert q1 + q2 == 2*HERTZ
    assert q2 + q3 == 2*HERTZ
    assert q3 + q1 == 2*HERTZ
    with should_throw(TypeError):
        NEWTON + NEWTON

    q = 100*WATT * 10*PERCENT
    assert q.value == 1000
    assert q.to(WATT).value == 10
    q = 100*WATT * (10*PERCENT)
    assert q.value == 1000
    
    assert 1*METER*(KILOGRAM/SECOND**2) == 1*NEWTON
    
    assert (1*METER*KILOGRAM/(METER*PASCAL)).unit.symbol == 'm.kg/(m.P)'
    assert 5*PERCENT*2 == 0.10
    str(5*PERCENT*(5*PERCENT))
    assert 1*WATT == 1000*MILLIWATT
    assert 1*WATT > 500*MILLIWATT
    assert not 1*WATT < 500*MILLIWATT
    assert 5*METER*METER*5 == 250000*CENTIMETER**2
    assert (5*METER)**2 == (500*CENTIMETER)**2
    assert 23*CENTIMETER**2 == 23*(CENTIMETER**2)
    '''
    assert repr(CENTIMETER**2) == 'x'
    type(5*CENTIMETER)
    print repr(5*CENTIMETER)
    print repr(5*CENTIMETER*CENTIMETER)
    print repr( LengthQuantity(5,CENTIMETER) )
    print repr(1*KILOMETER + 1*NANOMETER  )
    print CENTIMETER
    assert 4*KELVIN-6*KELVIN == -2*KELVIN
    '''
        

test()



