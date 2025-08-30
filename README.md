# Tarifa PT (Home Assistant)

Exponha 5 sensores com base nos períodos horários da **ERSE (Portugal Continental)**.

- `tarrif-now` (string): período atual (`vazio`, `fora_vazio`, `cheias`, `ponta`)
- `next-tarrif` (string): próximo período
- `tarrif-now-elapsed` (min): minutos decorridos
- `tarrif-now-remaing` (min): minutos restantes até mudança
- `next-tarrif-durantion` (min): duração do próximo período

## Modos suportados
- `bi_semanal` (bi-horária semanal)
- `bi_diario` (bi-horária diária: vazio 22:00–08:00)
- `tri_diario` (tri-horária diária: verão/inverno)

## Instalação manual
1. Copiar `custom_components/tarifa_pt` para `config/custom_components/`.
2. Reiniciar o Home Assistant.
3. Em `configuration.yaml`:
```yaml
sensor:
  - platform: tarifa_pt
    mode: bi_semanal   # ou: bi_diario | tri_diario
```
4. Reiniciar novamente.

## Via HACS (Custom Repository)
- HACS → Integrations → ⋯ → **Custom repositories**
- Repository: `https://github.com/SkywalkerPTE419/ha-tarifa-pt`
- Category: **Integration**
- Instalar e reiniciar.
