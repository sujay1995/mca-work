<!DOCTYPE html  >
<html>
<head>
    <meta charset="UTF-8">
    <title>Converter</title>
    <link rel="stylesheet" type="text/css" href="asset/bootstrap.min.css">
</head>
<body>
<div class="container">
    <div class="page-header">
        <h2>Converter</h2>
    </div>
    <div class="panel panel-primary">
        <div class="panel-heading">
            Length

        </div>
        <div class="panel-body">
            <form id="Angle">
                <input type="hidden" id="type" value="Length">
                <div class="form-group col-md-2">
                    <label>Value</label>
                    <input type="text" id="value" class="form-control">
                </div>
                <div class="form-group col-md-4">
                    <label>From</label>
                    <select class="form-control" id="from">
                        <option value="grad">^grad</option>
                        <option value="rad">radians</option>
                        <option value="degree">degree</option>
                        <option value="minutes">minutes</option>
                        <option value="seconds">seconds</option>
                        <option value="points">points</option>


                    </select>

                </div>
                <div class="form-group col-md-4">
                    <label>To</label>
                    <select class="form-control" id="to">
                      <option value="grad">^grad</option>
                      <option value="rad">radians</option>
                      <option value="degree">degree</option>
                      <option value="minutes">minutes</option>
                      <option value="seconds">seconds</option>
                      <option value="points">points</option>
                    </select>
                </div>
                <div class="form-group col-md-2">
                    <label>&nbsp;</label>
                    <input type="submit" class=" form-control btn btn-primary" value="Convert"/>
                </div>

                <div class="col-md-12  text-center">
                    <br/>
                    <span class="alert alert-info" id="result"> <i class="fa fa-question" aria-hidden="true"></i> Please select the value and click Convert</span><br/><br/>
                </div>

            </form>
        </div>





</body>
</html>
<?php
include "external.html";
?>
