# Tarifa PT (Home Assistant)

Integração simples para expor 5 sensores com base nos períodos horários da **ERSE (Portugal Continental)**:

- `tarrif-now` (string): período atual
- `next-tarrif` (string): próximo período
- `tarrif-now-elapsed` (min): minutos decorridos
- `tarrif-now-remaing` (min): minutos restantes
- `next-tarrif-durantion` (min): duração total do próximo período

## Modos suportados
- `bi_semanal`
- `bi_diario`
- `tri_diario`

## Instalação
1. Copiar `custom_components/tarifa_pt` para `config/custom_components`.
2. Reiniciar o Home Assistant.
3. Em `configuration.yaml`:
```yaml
sensor:
  - platform: tarifa_pt
    mode: bi_semanal
```
4. Reiniciar novamente.

## Via HACS
1. HACS → Integrations → Custom repositories
2. Adicionar `https://github.com/SkywalkerPTE419/ha-tarifa-pt` como **Integration**
3. Instalar e reiniciar HA

---
by @SkywalkerPTE419
