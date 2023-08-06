window.onload = function() {
 var myvalues = [515, 519, 520, 522, 652, 810, 370, 627, 319, 630, 921];
  $('#chartContainer').sparkline(myvalues, {
    type     : 'line',
    lineColor: '#92c1dc',
    fillColor: '#ebf4f9',
    height   : '50',
    width    : '80'
  });

}