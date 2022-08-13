var calculate = function(str) 
{
    let str = str.replace(/[^-()\d/*+.]/g, '') // regex for assure that eval will be safe
    try
    {
        var res = (typeof eval(str) == 'number') ? eval(str) : 'Error :(' 
        return res
    } catch (SyntaxError) { return 'Error :(' } // Ex. 1+5+6 It will ignore JS-SyntaxError
}
