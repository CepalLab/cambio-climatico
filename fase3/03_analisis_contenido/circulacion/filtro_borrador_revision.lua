function Para(element)
  local text = pandoc.utils.stringify(element)
  if text:match("^Borrador v2 para revisión editorial%.") then
    return {}
  end
  if text:match("^La verificación reproducible de ejes se conserva") then
    return pandoc.read(
      "Los materiales de respaldo técnico, las verificaciones y los registros de trazabilidad se conservan en los archivos de trabajo del proyecto.",
      "markdown"
    ).blocks[1]
  end
end

function Blocks(blocks)
  local filtered = {}
  local skip = false

  for _, block in ipairs(blocks) do
    if block.t == "Header" and block.level == 2 then
      local title = pandoc.utils.stringify(block)
      if title == "Figuras y cuadros" or title == "Anexo técnico" then
        skip = true
      elseif not skip then
        table.insert(filtered, block)
      end
    elseif block.t == "Header" and block.level == 1 then
      skip = false
      table.insert(filtered, block)
    elseif not skip then
      table.insert(filtered, block)
    end
  end

  return filtered
end