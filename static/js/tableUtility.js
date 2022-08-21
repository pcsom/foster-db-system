var orders = {}
function sortTable(n)
{
    var starter = performance.now()
    if (orders[n.toString()] == null)
        orders[n.toString()] = true
    else
        orders[n.toString()] = !orders[n.toString()]

    var table, rows, switching, i, x, y, dir, switchcount = 0, dataArr = []
    rows = $('#myTable tr')

    
    for (i = 1; i < rows.length; i++) 
    {
        x = $('td', rows.eq(i)).eq(n)
        var xData
        if (String(x.html())[0] == '<')
        {
            if (String(x.html()).slice(0,4) == '<sel')
            {
                xData = $('option:selected', x.children().eq(0)).text()
            }
            else
            {
                xData = x.children().eq(0).val()
            }
        }
        else
        {
            xData = x.text()
        }
        //dataArr.push([xData.toLowerCase(), i])
        if (!isNaN(xData) && !isNaN(parseFloat(xData)))
        {
            xData = Number(xData)
            dataArr.push([xData, i])
        }
        else
        {
            dataArr.push([xData.toLowerCase(), i])
        }
    }

    mergeSort(dataArr, 0, dataArr.length-1, n.toString())
    var tbody = $('#myTable tbody')

    for (i = 0; i < dataArr.length; i++)
    {
        tbody.append(rows.eq(dataArr[i][1]))
    }
    var ender = performance.now()
    console.log(`took ${ender-starter} ms to sort`)
}





function merge(arr, l, m, r, ind) {
    var n1 = m - l + 1;
    var n2 = r - m;

    // Create temp arrays
    var L = new Array(n1);
    var R = new Array(n2);

    // Copy data to temp arrays L[] and R[]
    for (var i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (var j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];


    // Merge the temp arrays back into arr[l..r]

    // Initial index of first subarray
    var i = 0;

    // Initial index of second subarray
    var j = 0;

    // Initial index of merged subarray
    var k = l;

    if (orders[ind])
    {
        while (i < n1 && j < n2) {
            if (L[i][0] <= R[j][0]) {
                arr[k] = L[i];
                i++;
            }
            else {
                arr[k] = R[j];
                j++;
            }
            k++;
        }
    }
    else
    {
        while (i < n1 && j < n2) {
            if (L[i][0] >= R[j][0]) {
                arr[k] = L[i];
                i++;
            }
            else {
                arr[k] = R[j];
                j++;
            }
            k++;
        }
    }
    

    // Copy the remaining elements of
    // L[], if there are any
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    // Copy the remaining elements of
    // R[], if there are any
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }

}

// l is for left index and r is
// right index of the sub-array
// of arr to be sorted */
function mergeSort(arr, l, r, ind) {
    if (l >= r) {
        return;             //returns recursively
    }
    var m = l + parseInt((r - l) / 2)
    mergeSort(arr, l, m, ind)
    mergeSort(arr, m + 1, r, ind)
    merge(arr, l, m, r, ind)
}






jQuery.expr[':'].icontains = function(a, i, m) {
    return jQuery(a).text().toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
}


var rows
var toSearch = [], theInd = 0, validCells, isVal, plural

function setupFilters(numInd, plur)
{
    plural = plur

    for (var i = 0; i < numInd; i++)
    {
        toSearch.push("")
    }

    $('.sBar').val('')

    $('.sBar').on('input', function() {
        toSearch[Number($(this).attr('id').slice('3'))] = $(this).val()
    })

    $('.sBar').on('keypress', function(e) {
        if (e.which == 13)
        {
            makeChange()
        }
    })

    $('#goSearch').on('click', function() {
        makeChange()
    })

    $('#clearFil').on('click', function(){
        $('.sBar').val("")
        for (var i = 0; i < toSearch.length; i++)
        {
            toSearch[i] = ""
        }
    })
}

function makeChange()
{
    var curStr = ""
    allVal = true
    for(var i=0; i < toSearch.length; i++)
    {
        if (toSearch[i] != "")
        {
            allVal = false
            curStr += `:has(td:nth-child(${i+1}):icontains('${toSearch[i]}'))`
        }
    }
    if (allVal)
    {
        validRows = rows
        rows.show()
    }
    else
    {
        validRows = rows.filter(curStr)
        validRows.show()
        rows.not(validRows).hide()
    }
    
    $('#matchCount').text(`${validRows.length} ${plural} match the current search filters`)
}
