<?php

$x = 5;
$name = "phu";

$gpa = 3.5;

echo var_dump($gpa);

echo var_dump($x);

$cars = array("he", "d", "s");

$products = ["2", "2", "d"];

echo var_dump($products);

echo var_dump($cars);


$gender = false;

echo var_dump($gender);

echo var_dump($name);




class Car {
    public $color;
    public $model;


    public function __construct($color, $model) {
        $this->color = $color;
        $this->model = $model;
    }

    public function message() {
        return "My car is a ". $this->color . " " . $this->model . "!";
    }

}

$myCar = new Car("red", "volvo");

echo var_dump($myCar);


$hehe = NULL;

echo var_dump($hehe);

?>