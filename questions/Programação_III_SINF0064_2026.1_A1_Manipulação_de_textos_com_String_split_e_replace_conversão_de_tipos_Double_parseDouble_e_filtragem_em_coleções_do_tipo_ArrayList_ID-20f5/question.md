(0,5 ponto) Analise o trecho de código abaixo que simula parte de um Sistema de Monitoramento de Enchentes Urbanas:

```java
ArrayList<String> historico = new ArrayList<String>();
historico.add("Sensor_A01:12.5mm");
historico.add("Sensor_B02:45.0mm");
historico.add("Sensor_A01:52.1mm");
historico.add("Sensor_C03:8.2mm");

ArrayList<String> alertas = new ArrayList<String>();
for (String registro : historico) {
    String[] partes = registro.split(":");
    String valorTexto = partes[1].replace("mm", "");
    double milimetros = Double.parseDouble(valorTexto);
    if (milimetros > 40.0) {
        alertas.add(partes[0].toUpperCase());
    }
}

System.out.println(alertas.get(0) + " e " + alertas.get(1));

```

Após a execução completa do método, a saída impressa no console correspondente será:

a) SENSOR_A01 e SENSOR_C03

b) Exceção do tipo IndexOutOfBoundsException.

c) SENSOR_B02 e SENSOR_A01

d) Sensor_B02 e Sensor_A01

e) Sensor_A01:12.5mm e Sensor_A01:52.1mm