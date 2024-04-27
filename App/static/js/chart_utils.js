const Meses_Label = [
          'Enero',
          'Febrero',
          'Marzo',
          'Abril',
          'Mayo',
          'Junio',
          'Julio',
          'Agosto',
          'Septiembre',
          'Octubre',
          'Noviembre',
          'Diciembre'
        ];

const Meses_django = ['ene', 'feb', 'mar', 'abr', 'may', 'jun',
    'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];

let indiceMes = 11;


function inicializar_meses(){
    const diccionario = {};
    Meses_django.forEach(mes => {
        diccionario[mes] = 0;
    });
    return diccionario
}

function months_label(mes_actual) {
    return Meses_Label.slice(0, mes_actual)
}

function mesAnteriorValor(year, mes) {
    const meses = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];
    const indiceMes = meses.indexOf(mes);

    // Si el mes es enero, el año anterior
    if (indiceMes === 0) {
        const YearBefore = (parseInt(year) - 1).toString();
        const lastMonthYearBefore = datos[YearBefore]["dic"]; // Diciembre del año anterior
        return { "dic": lastMonthYearBefore };
    }

    // Si el mes no es enero, simplemente se devuelve el mes anterior
    const mesAnterior = meses[indiceMes - 1];
    return { [mesAnterior]: datos[year][mesAnterior] };
}


function addData(chart, newData) {
    if (chart.data.labels.length < 14){
        console.log(chart.data.labels[0])
        chart.data.labels.unshift(Meses_Label[indiceMes]);
        chart.data.datasets[0].data.unshift(newData[0]);
        chart.data.datasets[1].data.unshift(newData[1]);
        indiceMes = (indiceMes -1 + Meses_Label.length) % Meses_Label.length;
    }
    chart.update();
}

function removeData(chart) {
    if (chart.data.labels.length > 4){
        chart.data.labels.shift();
        chart.data.datasets.forEach((dataset) => {
            dataset.data.shift();
        });
        indiceMes++;
    }
    chart.update();
}

