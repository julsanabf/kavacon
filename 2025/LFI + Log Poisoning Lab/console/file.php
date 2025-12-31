<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Visor de Archivos</title>
    <style>
        body { font-family: monospace; background-color: #f4f4f4; }
        .container { padding: 20px; }
        .file-content {
            background-color: #fff;
            border: 1px solid #ddd;
            padding: 15px;
            white-space: pre-wrap; /* Mantiene el formato del texto */
            word-wrap: break-word;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Contenido del Archivo Solicitado:</h2>
        <div class="file-content">
            <?php
                // Obtiene el nombre del archivo desde el parámetro GET 'file'
                $file = $_GET['file'];

                // ¡ADVERTENCIA! La siguiente línea es deliberadamente vulnerable a LFI.
                // Nunca uses este código en un entorno de producción.
                if (isset($file)) {
                    include($file);
                } else {
                    echo "Por favor, especifique un archivo a través del parámetro '?file='.";
                }
            ?>
        </div>
    </div>
</body>
</html>
