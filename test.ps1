

function TestInContainer($name) {
    $TAG="python_magic/${name}:latest"
    docker build -t $TAG -f "test/Dockerfile_${name}" .
    docker run "python_magic/${name}:latest"
}

TestInContainer "xenial"
TestInContainer "bionic"
TestInContainer "focal"