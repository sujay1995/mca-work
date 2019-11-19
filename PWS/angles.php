<?php

class Angle
{

    private $from;
    private $to;
    private $value;

    public function __construct($from, $to, $value)
    {
        $this->from = $from;
        $this->to = $to;
        $this->value = $value;
    }

    public function convert()
    {
        return $this->convert();

    }

    private function convert()
    {
        $val = $this->convertToGrad();
        switch ($this->to) {
            case '^grad':
                return (double)$val;
                break;
            case 'rad':
                return (double)$val * 63.661977237;
                break;
            case 'degree':
                return (double)$val *0.9 ;
                break;
            case 'minutes':
                return (double)$val * 54;
                break;
            case 'seconds':
                return (double)$val * 3240 ;
                break;
            case 'point':
                return (double)$val * 0.08;
                break;

        }
    }

    private function convertToGrad()
    {
        switch ($this->from) {
            case '^grad':
                return (double)$this->value;
                break;
            case 'rad':
                return (double)$this->value * 0.0174532925;
                break;
            case 'degree':
                return (double)$this->value *  1.1111111111;
                break;
            case 'minutes':
                return (double)$this->value *  0.0185185185;
                break;
            case 'seconds':
                return (double)$this->value * 0.000308642 ;
                break;
            case 'points':
                return (double)$this->value * 12.5;
                break;


        }
    }
}
?>
