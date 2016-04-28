Date.prototype.getMonthName = function(){ return (["January","February","March","April","May","June","July","August","September","October","November","December"])[this.getMonth()]; }

Date.prototype.toLocaleFormat = Date.prototype.toLocaleFormat || function(pattern) {
    return pattern.replace(/%Y/g, this.getFullYear()).replace(/%m/g, (this.getMonth() + 1)).replace(/%d/g, this.getDate()>9?this.getDate():'0'+this.getDate()).replace(/%B/g, (this.getMonthName()));
};

function startsplash()
{
    stopsplash();
    //alert("startsplash");
    $('#dvLoading').show();
    setTimeout(stopsplash,3000000);

}
function stopsplash(secs)
{
    //alert("stopsplash");
     $('#dvLoading').fadeOut(secs);
}
