pipeline {
    agent any

    options {
        buildDiscarder(
            logRotator(
                numToKeepStr: '10',
                artifactNumToKeepStr: '5'
            )
        )

        timeout(time: 20, unit: 'MINUTES')
        timestamps()
        disableConcurrentBuilds()
    }

    parameters {
        string(
            name: 'BRANCH_NAME',
            defaultValue: 'main',
            description: 'Git branch to build'
        )
    }

    triggers {
        githubPush()
    }

    environment {
        // Project
        FRONTEND_DIR = 'frontend'
        UAT_ROOT = 'C:\\TaskPilot-UAT'
        PROD_ROOT = 'C:\\TaskPilot-PROD'

        // Python
        PYTHON_EXE = 'python'
        NODE_EXE = 'node'
        NPM_EXE = 'npm.cmd'
        GIT_EXE = 'git.exe'
        VENV_DIR = "${WORKSPACE}\\.venv"
        PYTHONPATH = "${WORKSPACE}"

        // MySQL / Database Configuration (DO NOT include passwords here - use Jenkins Credentials)
        DB_HOST = '127.0.0.1'
        DB_PORT = '3306'
        DB_USER = 'root'
        DB_NAME = 'task_pilot'

        // Production Configuration
        PROD_PORT = '5001'
        PROD_ENV = 'production'
    }

    stages {

        // =========================================================
        // 1. CHECKOUT
        // =========================================================
        stage('Checkout') {
            steps {
                echo '=================================================='
                echo '              TASKPILOT CHECKOUT'
                echo '=================================================='

                // Jenkins already performs the SCM checkout
                // because the job uses "Pipeline script from SCM".

                bat '''
                    echo Workspace:
                    echo "%WORKSPACE%"

                    echo.
                    echo Current Git revision:
                    git rev-parse --short HEAD

                    echo.
                    echo Current branch:
                    git branch --show-current
                '''

                echo 'Repository checkout completed.'
            }
        }

        // =========================================================
        // 2. PREFLIGHT VALIDATION
        // =========================================================
        stage('Preflight Validation') {
            steps {
                echo '=================================================='
                echo '             PREFLIGHT VALIDATION'
                echo '=================================================='

                script {
                    try {
                        withCredentials([
                            usernamePassword(credentialsId: 'taskpilot-uat-db',
                                           usernameVariable: 'PREFLIGHT_UAT_DB_USER',
                                           passwordVariable: 'PREFLIGHT_UAT_DB_PASSWORD'),
                            string(credentialsId: 'taskpilot-uat-secret-key',
                                  variable: 'PREFLIGHT_UAT_SECRET_KEY')
                        ]) {
                            bat '''
                                setlocal
                                echo TaskPilot CI/CD
                                echo Branch: %BRANCH_NAME%
                                echo Jenkins workspace: %WORKSPACE%
                                echo Frontend: %FRONTEND_DIR%
                                echo Build type: production
                                echo Environment: UAT then PROD after approval

                                if not exist "%WORKSPACE%" (
                                    echo ERROR: Jenkins workspace does not exist: %WORKSPACE%
                                    exit /b 1
                                )
                                if not exist "%WORKSPACE%\\.git" (
                                    echo ERROR: Repository was not checked out in the Jenkins workspace.
                                    exit /b 1
                                )
                                if not exist "%WORKSPACE%\\requirements.txt" (
                                    echo ERROR: requirements.txt was not found.
                                    echo Action: Verify the repository checkout and branch configuration.
                                    exit /b 1
                                )
                                if not exist "%WORKSPACE%\\frontend\\package.json" (
                                    echo ERROR: frontend\\package.json was not found.
                                    exit /b 1
                                )
                                if not exist "%WORKSPACE%\\frontend\\package-lock.json" (
                                    echo ERROR: frontend\\package-lock.json is required for deterministic npm ci.
                                    echo Action: Commit the lockfile before running CI.
                                    exit /b 1
                                )
                                if not exist "%WORKSPACE%\\app.py" (
                                    echo ERROR: app.py was not found.
                                    exit /b 1
                                )
                                if not exist "%WORKSPACE%\\database.py" (
                                    echo ERROR: database.py was not found.
                                    exit /b 1
                                )
                                if "%DB_HOST%"=="" (
                                    echo ERROR: DB_HOST is not configured.
                                    exit /b 1
                                )
                                if "%DB_PORT%"=="" (
                                    echo ERROR: DB_PORT is not configured.
                                    exit /b 1
                                )
                                if "%DB_NAME%"=="" (
                                    echo ERROR: DB_NAME is not configured.
                                    exit /b 1
                                )

                                where "%PYTHON_EXE%" >nul 2>&1
                                if errorlevel 1 (
                                    echo ERROR: Python executable was not found: %PYTHON_EXE%
                                    echo Action: Configure Python on the Jenkins service PATH or set PYTHON_EXE in the job environment.
                                    exit /b 1
                                )
                                "%PYTHON_EXE%" --version
                                if errorlevel 1 (
                                    echo ERROR: Python could not be started: %PYTHON_EXE%
                                    exit /b 1
                                )
                                "%PYTHON_EXE%" -m pip --version
                                if errorlevel 1 (
                                    echo ERROR: pip is unavailable for %PYTHON_EXE%.
                                    exit /b 1
                                )

                                where "%NODE_EXE%" >nul 2>&1
                                if errorlevel 1 (
                                    echo ERROR: Node.js executable was not found: %NODE_EXE%
                                    echo Action: Configure Node.js on the Jenkins service PATH.
                                    exit /b 1
                                )
                                "%NODE_EXE%" --version
                                if errorlevel 1 (
                                    echo ERROR: Node.js could not be started.
                                    exit /b 1
                                )
                                where "%NPM_EXE%" >nul 2>&1
                                if errorlevel 1 (
                                    echo ERROR: npm executable was not found: %NPM_EXE%
                                    echo Action: Configure npm on the Jenkins service PATH.
                                    exit /b 1
                                )
                                "%NPM_EXE%" --version
                                if errorlevel 1 (
                                    echo ERROR: npm could not be started.
                                    exit /b 1
                                )

                                where "%GIT_EXE%" >nul 2>&1
                                if errorlevel 1 (
                                    echo ERROR: Git executable was not found: %GIT_EXE%
                                    echo Action: Configure Git on the Jenkins service PATH or fix Jenkins Git tool configuration.
                                    exit /b 1
                                )
                                "%GIT_EXE%" --version
                                if errorlevel 1 (
                                    echo ERROR: Git could not be started.
                                    exit /b 1
                                )

                                echo UAT credentials resolved successfully without displaying secret values.
                                echo Preflight validation completed successfully.
                            '''
                        }
                    } catch (Exception preflightError) {
                        error('PREFLIGHT VALIDATION FAILED. Verify Jenkins global credentials taskpilot-uat-db and taskpilot-uat-secret-key, the Jenkins service PATH, and the required repository files. Secret values are intentionally never printed.')
                    }
                }
            }
        }

        // =========================================================
        // 3. BACKEND SETUP
        // =========================================================
        stage('Backend Setup') {
            steps {
                echo '=================================================='
                echo '              BACKEND SETUP'
                echo '=================================================='

                bat '''
                    echo Python executable:
                    "%PYTHON_EXE%" --version

                    if errorlevel 1 (
                        echo ERROR: Python executable could not be started.
                        exit /b 1
                    )

                    echo.
                    echo Pip:
                    "%PYTHON_EXE%" -m pip --version

                    if errorlevel 1 (
                        echo ERROR: pip is not available.
                        exit /b 1
                    )

                    echo.
                    echo Checking requirements.txt...

                    if not exist "%WORKSPACE%\\requirements.txt" (
                        echo ERROR: requirements.txt was not found.
                        exit /b 1
                    )

                    echo requirements.txt found.

                    echo.
                    echo Removing old virtual environment...

                    if exist "%VENV_DIR%" (
                        rmdir /S /Q "%VENV_DIR%"
                        if errorlevel 1 (
                            echo ERROR: Failed to remove the stale virtual environment.
                            exit /b 1
                        )
                    )

                    echo.
                    echo Creating Python virtual environment...

                    "%PYTHON_EXE%" -m venv "%VENV_DIR%"

                    if errorlevel 1 (
                        echo ERROR: Failed to create virtual environment.
                        exit /b 1
                    )

                    if not exist "%VENV_DIR%\\Scripts\\python.exe" (
                        echo ERROR: Virtual environment Python executable was not created.
                        exit /b 1
                    )

                    if not exist "%VENV_DIR%\\Scripts\\pip.exe" (
                        echo ERROR: Virtual environment pip executable was not created.
                        exit /b 1
                    )

                    echo.
                    echo Virtual environment created successfully.

                    echo.
                    echo Virtual environment Python:
                    "%VENV_DIR%\\Scripts\\python.exe" --version

                    echo.
                    echo Upgrading pip...

                    "%VENV_DIR%\\Scripts\\python.exe" -m pip install --upgrade pip setuptools wheel

                    if errorlevel 1 (
                        echo ERROR: Failed to upgrade pip.
                        exit /b 1
                    )

                    echo.
                    echo Installing backend dependencies...

                    "%VENV_DIR%\\Scripts\\python.exe" -m pip install -r "%WORKSPACE%\\requirements.txt"

                    if errorlevel 1 (
                        echo ERROR: Backend dependency installation failed.
                        exit /b 1
                    )

                    echo.
                    echo Installing pytest...

                    "%VENV_DIR%\\Scripts\\python.exe" -m pip install pytest pytest-cov

                    if errorlevel 1 (
                        echo ERROR: pytest installation failed.
                        exit /b 1
                    )

                    echo.
                    echo Backend environment ready.
                '''
            }
        }

        // =========================================================
        // 3. BACKEND TESTS
        // =========================================================
        stage('Backend Tests') {
            steps {
                echo '=================================================='
                echo '              BACKEND TESTS'
                echo '=================================================='

                bat '''
                    if not exist "%VENV_DIR%\\Scripts\\python.exe" (
                        echo ERROR: Virtual environment does not exist.
                        exit /b 1
                    )

                    if exist "%WORKSPACE%\\tests" (

                        echo Tests directory found.
                        echo Running pytest...

                        "%VENV_DIR%\\Scripts\\python.exe" -m pytest "%WORKSPACE%\\tests" -v --tb=short

                        if errorlevel 1 (
                            echo ERROR: Backend tests failed.
                            exit /b 1
                        )

                        echo.
                        echo Backend tests passed successfully.

                    ) else (

                        echo No tests directory found.
                        echo Running Python syntax validation...

                        "%VENV_DIR%\\Scripts\\python.exe" -m compileall -q "%WORKSPACE%"

                        if errorlevel 1 (
                            echo ERROR: Python syntax validation failed.
                            exit /b 1
                        )

                        echo Python syntax validation passed.
                    )
                '''
            }
        }

        // =========================================================
        // 4. FRONTEND SETUP
        // =========================================================
        stage('Frontend Setup') {
            steps {
                echo '=================================================='
                echo '              FRONTEND SETUP'
                echo '=================================================='

                bat '''
                    cd /d "%WORKSPACE%\\%FRONTEND_DIR%"

                    echo Frontend directory:
                    cd

                    echo.
                    echo Checking package.json...

                    if not exist "package.json" (
                        echo ERROR: frontend\\package.json was not found.
                        exit /b 1
                    )

                    echo package.json found.

                    echo.
                    echo Node version:
                    "%NODE_EXE%" --version

                    if errorlevel 1 (
                        echo ERROR: Node.js is not available to Jenkins.
                        exit /b 1
                    )

                    echo.
                    echo npm version:
                    "%NPM_EXE%" --version

                    if errorlevel 1 (
                        echo ERROR: npm is not available to Jenkins.
                        exit /b 1
                    )

                    echo.
                    echo Checking npm configuration...

                    "%NPM_EXE%" config get registry

                    echo.
                    echo Removing old node_modules...

                    if exist "node_modules" (
                        rmdir /S /Q "node_modules"
                        if errorlevel 1 (
                            echo ERROR: Failed to remove stale frontend dependencies.
                            exit /b 1
                        )
                    )

                    echo.
                    echo Installing frontend dependencies...

                    if exist "package-lock.json" (

                        echo package-lock.json found.
                        echo Running npm ci...

                        "%NPM_EXE%" ci --no-audit --no-fund

                        if errorlevel 1 (
                            echo ERROR: npm ci failed.
                            exit /b 1
                        )

                    ) else (
                        echo ERROR: package-lock.json is required; npm install is not permitted in CI.
                        exit /b 1
                    )
                    echo.
                    echo Verifying node_modules...

                    if not exist "node_modules" (
                        echo ERROR: node_modules directory was not created.
                        exit /b 1
                    )

                    echo node_modules created successfully.

                    echo.
                    echo Checking Vite package...

                    "%NPM_EXE%" ls vite --depth=0

                    if errorlevel 1 (
                        echo ERROR: Vite is not installed as a project dependency.
                        echo.
                        echo package.json dependencies:
                        type package.json
                        exit /b 1
                    )

                    echo.
                    echo Checking Vite executable...

                    if not exist "node_modules\\.bin\\vite.cmd" (
                        echo ERROR: node_modules\\.bin\\vite.cmd was not created.
                        echo.
                        echo Contents of node_modules\\.bin:
                        dir "node_modules\\.bin"
                        exit /b 1
                    )

                    echo Vite executable found successfully.

                    echo.
                    echo Testing Vite version...

                    for /f "delims=" %%v in ('"%NODE_EXE%" -p "require('./node_modules/vite/package.json').version"') do set "VITE_VERSION=%%v"
                    if not "%VITE_VERSION%"=="5.4.21" (
                        echo ERROR: Vite version mismatch. Expected 5.4.21 from package-lock.json, found %VITE_VERSION%.
                        exit /b 1
                    )

                    node_modules\\.bin\\vite.cmd --version

                    if errorlevel 1 (
                        echo ERROR: Local Vite executable could not run.
                        exit /b 1
                    )

                    echo.
                    echo Frontend setup completed successfully.
                '''
            }
        }

        // =========================================================
        // 5. FRONTEND BUILD
        // =========================================================
        stage('Frontend Build') {
            steps {
                echo '=================================================='
                echo '              FRONTEND BUILD'
                echo '=================================================='

                bat '''
                    cd /d "%WORKSPACE%\\%FRONTEND_DIR%"

                    echo Checking if frontend dependencies are installed...

                    if not exist "node_modules\\.bin\\vite.cmd" (
                        echo ERROR: Local Vite executable is missing. Frontend Setup should have installed it with npm ci.
                        exit /b 1
                    )

                    if not exist "package-lock.json" (
                        echo ERROR: package-lock.json is required for the production build.
                        exit /b 1
                    )

                    echo.
                    echo Running frontend production build...
                    "%NPM_EXE%" run build

                    if errorlevel 1 (
                        echo ERROR: Vite production build failed.
                        exit /b 1
                    )

                    echo.
                    echo Verifying build output...

                    if not exist "dist" (
                        echo ERROR: dist directory was not created.
                        exit /b 1
                    )

                    if not exist "dist\\index.html" (
                        echo ERROR: frontend\\dist\\index.html was not created.
                        exit /b 1
                    )

                    echo.
                    echo Frontend build completed successfully.

                    echo.
                    echo Build output:
                    dir "dist"
                '''
            }
        }

        // =========================================================
        // 6. PACKAGE APPLICATION
        // =========================================================
        stage('Package Application') {
            steps {
                echo '=================================================='
                echo '             PACKAGE APPLICATION'
                echo '=================================================='

                bat '''
                    setlocal enabledelayedexpansion

                    set "PACKAGE_ROOT=%UAT_ROOT%\\releases\\TaskPilot-UAT-%BUILD_NUMBER%"
                    set "PACKAGE_ZIP=%UAT_ROOT%\\releases\\TaskPilot-UAT-%BUILD_NUMBER%.zip"

                    if exist "%UAT_ROOT%" (
                        rmdir /S /Q "%UAT_ROOT%"
                    )

                    mkdir "%UAT_ROOT%"
                    mkdir "%UAT_ROOT%\\releases"
                    mkdir "%UAT_ROOT%\\logs"

                    if not exist "%WORKSPACE%\\requirements.txt" (
                        echo ERROR: requirements.txt is missing from the repository.
                        exit /b 1
                    )

                    if not exist "%WORKSPACE%\\%FRONTEND_DIR%\\dist\\index.html" (
                        echo ERROR: Frontend dist index.html is missing.
                        exit /b 1
                    )

                    echo Copying Python backend files...
                        xcopy /E /I /Y "%WORKSPACE%\\*.py" "%PACKAGE_ROOT%\" >nul
                        if errorlevel 1 (
                            echo ERROR: Failed to copy Python backend files into the package.
                            exit /b 1
                        )
                        xcopy /E /I /Y "%WORKSPACE%\\requirements.txt" "%PACKAGE_ROOT%\" >nul
                        if errorlevel 1 (
                            echo ERROR: Failed to copy requirements.txt into the package.
                            exit /b 1
                        )
                    echo Creating runtime .env template for package...
                    (
                        echo FLASK_ENV=development
                        echo SECRET_KEY=__WILL_BE_SET_BY_JENKINS__
                        echo DB_HOST=%DB_HOST%
                        echo DB_PORT=%DB_PORT%
                        echo DB_USER=__WILL_BE_SET_BY_JENKINS__
                        echo DB_PASSWORD=__WILL_BE_SET_BY_JENKINS__
                        echo DB_NAME=%DB_NAME%
                    ) > "%PACKAGE_ROOT%\\.env"

                    echo Copying production frontend files...
                    xcopy /E /I /Y "%WORKSPACE%\\%FRONTEND_DIR%\\dist" "%PACKAGE_ROOT%\\%FRONTEND_DIR%\\dist\" >nul
                        if errorlevel 1 (
                            echo ERROR: Failed to copy frontend production files into the package.
                            exit /b 1
                        )

                    if not exist "%PACKAGE_ROOT%\\app.py" (
                        echo ERROR: Deployment package is missing app.py.
                        exit /b 1
                    )

                    if not exist "%PACKAGE_ROOT%\\%FRONTEND_DIR%\\dist\\index.html" (
                        echo ERROR: Deployment package is missing frontend dist index.html.
                        exit /b 1
                    )

                    echo Creating deployment zip artifact...
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; Compress-Archive -Path '%PACKAGE_ROOT%\\*' -DestinationPath '%PACKAGE_ZIP%' -Force"

                    if errorlevel 1 (
                        echo ERROR: Packaging failed.
                        exit /b 1
                    )

                    echo Package created successfully: %PACKAGE_ZIP%
                '''
            }
        }

        // =========================================================
        // 7. DEPLOYMENT PREFLIGHT
        // =========================================================
        stage('Deployment Preflight') {
            steps {
                echo '=================================================='
                echo '            DEPLOYMENT PREFLIGHT'
                echo '=================================================='

                bat '''
                    if not exist "%UAT_ROOT%\\releases\\TaskPilot-UAT-%BUILD_NUMBER%.zip" (
                        echo ERROR: UAT package archive is missing.
                        exit /b 1
                    )
                    if not exist "%UAT_ROOT%\\releases\\TaskPilot-UAT-%BUILD_NUMBER%\\app.py" (
                        echo ERROR: Packaged app.py is missing.
                        exit /b 1
                    )
                    if not exist "%UAT_ROOT%\\releases\\TaskPilot-UAT-%BUILD_NUMBER%\\%FRONTEND_DIR%\\dist\\index.html" (
                        echo ERROR: Packaged frontend\\dist\\index.html is missing.
                        exit /b 1
                    )
                    if not exist "%UAT_ROOT%" mkdir "%UAT_ROOT%"
                    if errorlevel 1 (
                        echo ERROR: UAT deployment root is unavailable: %UAT_ROOT%
                        exit /b 1
                    )
                    echo Package and UAT deployment prerequisites validated successfully.
                '''
            }
        }

        // =========================================================
        // 8. DEPLOY TO UAT
        // =========================================================
        stage('Deploy UAT') {
            steps {
                echo '=================================================='
                echo '               DEPLOY UAT'
                echo '=================================================='

                withCredentials([
                    usernamePassword(credentialsId: 'taskpilot-uat-db',
                                   usernameVariable: 'UAT_DEPLOY_DB_USER',
                                   passwordVariable: 'UAT_DEPLOY_DB_PASSWORD'),
                    string(credentialsId: 'taskpilot-uat-secret-key',
                          variable: 'UAT_DEPLOY_SECRET_KEY')
                ]) {
                bat '''
                    setlocal enabledelayedexpansion

                    set "PACKAGE_ROOT=%UAT_ROOT%\\releases\\TaskPilot-UAT-%BUILD_NUMBER%"
                    set "DEPLOY_DIR=%UAT_ROOT%\\current"

                    if exist "%DEPLOY_DIR%" (
                        rmdir /S /Q "%DEPLOY_DIR%"
                    )

                    xcopy /E /I /Y "%PACKAGE_ROOT%\\*" "%DEPLOY_DIR%\\*" >nul

                    if errorlevel 1 (
                        echo ERROR: UAT deployment copy failed.
                        exit /b 1
                    )

                    if not exist "%DEPLOY_DIR%\\app.py" (
                        echo ERROR: UAT deployment directory is missing app.py.
                        exit /b 1
                    )

                    echo UAT deployment completed: %DEPLOY_DIR%
                '''
                }
            }
        }

        // =========================================================
        // 8. UAT HEALTH / SMOKE TEST
        // =========================================================
        stage('UAT Health Check') {
            options {
                timeout(time: 60, unit: 'MINUTES')
            }
            steps {
                echo '=================================================='
                echo '           UAT HEALTH / SMOKE TEST'
                echo '=================================================='

                withCredentials([
                    usernamePassword(credentialsId: 'taskpilot-uat-db',
                                   usernameVariable: 'UAT_DB_USER',
                                   passwordVariable: 'UAT_DB_PASSWORD'),
                    string(credentialsId: 'taskpilot-uat-secret-key',
                          variable: 'UAT_SECRET_KEY')
                ]) {
                bat '''
                    setlocal enabledelayedexpansion

                    set "DEPLOY_DIR=%UAT_ROOT%\\current"
                    set "VENV_DIR=%DEPLOY_DIR%\\.venv"
                    set "LOG_FILE=%UAT_ROOT%\\logs\\taskpilot-uat.log"
                    set "PORT=5000"
                    set "DB_HOST=%DB_HOST%"
                    set "DB_PORT=%DB_PORT%"
                    set "DB_USER=%UAT_DB_USER%"
                    set "DB_PASSWORD=%UAT_DB_PASSWORD%"
                    set "DB_NAME=%DB_NAME%"

                    echo Writing UAT runtime configuration from Jenkins Credentials...
                    (
                        echo FLASK_ENV=development
                        echo SECRET_KEY=%UAT_SECRET_KEY%
                        echo DB_HOST=%DB_HOST%
                        echo DB_PORT=%DB_PORT%
                        echo DB_USER=%DB_USER%
                        echo DB_PASSWORD=%DB_PASSWORD%
                        echo DB_NAME=%DB_NAME%
                    ) > "%DEPLOY_DIR%\\.env"

                    echo Preparing the UAT runtime environment...
                    if exist "%VENV_DIR%" (
                        rmdir /S /Q "%VENV_DIR%"
                    )

                    "%PYTHON_EXE%" -m venv "%VENV_DIR%"
                    if errorlevel 1 (
                        echo ERROR: Failed to create the UAT virtual environment.
                        exit /b 1
                    )

                    "%VENV_DIR%\\Scripts\\python.exe" -m pip install --upgrade pip setuptools wheel
                    if errorlevel 1 (
                        echo ERROR: Failed to upgrade pip in UAT environment.
                        exit /b 1
                    )

                    "%VENV_DIR%\\Scripts\\python.exe" -m pip install -r "%DEPLOY_DIR%\\requirements.txt"
                    if errorlevel 1 (
                        echo ERROR: Failed to install backend dependencies in UAT environment.
                        exit /b 1
                    )

                    echo Initializing the UAT database and demo user...
                    "%VENV_DIR%\\Scripts\\python.exe" "%DEPLOY_DIR%\\database.py"
                    if errorlevel 1 (
                        echo ERROR: UAT database initialization failed.
                        exit /b 1
                    )

                    echo Stopping any previous TaskPilot UAT process on the health port...
                    for /f "tokens=1,2,3,4,5" %%a in ('netstat -ano ^| findstr :5000') do (
                        if not "%%e"=="" (
                            taskkill /PID %%e /F >nul 2>&1
                        )
                    )

                    if exist "%LOG_FILE%" (
                        del /Q "%LOG_FILE%"
                    )

                    echo Starting TaskPilot in the UAT environment...
                    start "TaskPilot-UAT" /B "%VENV_DIR%\\Scripts\\python.exe" "%DEPLOY_DIR%\\app.py" > "%LOG_FILE%" 2>&1

                    echo Waiting for the backend to start...
                    timeout /T 15 /NOBREAK >nul

                    echo Calling the TaskPilot health endpoint: http://127.0.0.1:5000/health
                    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
                        "$ErrorActionPreference='Stop'; " ^
                        "$response = Invoke-WebRequest -Uri 'http://127.0.0.1:5000/health' -UseBasicParsing -TimeoutSec 20; " ^
                        "if ($response.StatusCode -ne 200) { " ^
                            "throw 'Health check returned status code ' + $response.StatusCode " ^
                        "}; " ^
                        "$body = $response.Content; " ^
                        "Write-Host 'Response Body: ' $body; " ^
                        "if ($body -notmatch 'healthy') { " ^
                            "throw 'Health endpoint response does not contain healthy status' " ^
                        "}; " ^
                        "Write-Host 'UAT health check passed'"

                    if errorlevel 1 (
                        echo ERROR: UAT health check failed.
                        echo Showing UAT log output:
                        type "%LOG_FILE%"
                        exit /b 1
                    )

                    echo UAT deployment and health check passed successfully.
                '''
                }
            }
        }

        // =========================================================
        // 9. PRODUCTION APPROVAL
        // =========================================================
        stage('Production Approval') {
            steps {
                echo '=================================================='  
                echo '          PRODUCTION DEPLOYMENT APPROVAL'
                echo '=================================================='  
                echo ''
                echo 'UAT has passed successfully.'
                echo ''
                echo 'Ready to deploy to PRODUCTION?'
                echo ''
                echo 'This will deploy the application to:'
                echo 'Location: C:\\TaskPilot-PROD'
                echo 'Port:     5001'
                echo ''

                input(
                    id: 'ProductionApproval',
                    message: 'Deploy to PRODUCTION?',
                    ok: 'Deploy to PROD',
                    submitter: ''
                )

                echo 'PRODUCTION DEPLOYMENT APPROVED'
            }
        }

        // =========================================================
        // 11. DEPLOY PROD
        // =========================================================
        stage('Deploy PROD') {
            steps {
                echo '=================================================='
                echo '            DEPLOY TO PRODUCTION'
                echo '=================================================='

                withCredentials([
                    usernamePassword(credentialsId: 'taskpilot-prod-db',
                                   usernameVariable: 'PROD_DEPLOY_DB_USER',
                                   passwordVariable: 'PROD_DEPLOY_DB_PASSWORD'),
                    string(credentialsId: 'taskpilot-prod-secret-key',
                          variable: 'PROD_DEPLOY_SECRET_KEY')
                ]) {
                bat '''
                    setlocal enabledelayedexpansion

                    set "PACKAGE_ROOT=%UAT_ROOT%\\releases\\TaskPilot-UAT-%BUILD_NUMBER%"
                    set "PROD_DEPLOY_DIR=%PROD_ROOT%\\current"

                    if not exist "%PACKAGE_ROOT%" (
                        echo ERROR: Approved UAT artifact not found at %PACKAGE_ROOT%.
                        echo Possible causes: the package was removed or UAT did not complete.
                        exit /b 1
                    )
                    if not exist "%PACKAGE_ROOT%\\app.py" (
                        echo ERROR: Approved artifact is missing app.py.
                        exit /b 1
                    )
                    if not exist "%PACKAGE_ROOT%\\%FRONTEND_DIR%\\dist\\index.html" (
                        echo ERROR: Approved artifact is missing frontend\\dist\\index.html.
                        exit /b 1
                    )
                    if not exist "%PROD_ROOT%" mkdir "%PROD_ROOT%"
                    if errorlevel 1 (
                        echo ERROR: PROD deployment root is unavailable: %PROD_ROOT%.
                        exit /b 1
                    )

                    echo PROD credentials and approved artifact validated successfully.

                    echo Creating PROD environment structure...
                    if not exist "%PROD_ROOT%" (
                        mkdir "%PROD_ROOT%"
                    )

                    if not exist "%PROD_ROOT%\\releases" (
                        mkdir "%PROD_ROOT%\\releases"
                    )

                    if not exist "%PROD_ROOT%\\logs" (
                        mkdir "%PROD_ROOT%\\logs"
                    )

                    echo Removing previous PROD deployment...
                    if exist "%PROD_DEPLOY_DIR%" (
                        rmdir /S /Q "%PROD_DEPLOY_DIR%"
                    )

                    echo Copying UAT artifact to PROD...
                    xcopy /E /I /Y "%PACKAGE_ROOT%\\*" "%PROD_DEPLOY_DIR%\\*" >nul

                    if errorlevel 1 (
                        echo ERROR: PROD deployment copy failed.
                        exit /b 1
                    )

                    if not exist "%PROD_DEPLOY_DIR%\\app.py" (
                        echo ERROR: PROD deployment directory is missing app.py.
                        exit /b 1
                    )

                    echo PROD deployment copied successfully: %PROD_DEPLOY_DIR%
                '''
                }
            }
        }

        // =========================================================
        // 11. PROD HEALTH CHECK
        // =========================================================
        stage('PROD Health Check') {
            options {
                timeout(time: 60, unit: 'MINUTES')
            }
            steps {
                echo '=================================================='
                echo '         PRODUCTION HEALTH / SMOKE TEST'
                echo '=================================================='

                withCredentials([
                    usernamePassword(credentialsId: 'taskpilot-prod-db',
                                   usernameVariable: 'PROD_DB_USER',
                                   passwordVariable: 'PROD_DB_PASSWORD'),
                    string(credentialsId: 'taskpilot-prod-secret-key',
                          variable: 'PROD_SECRET_KEY')
                ]) {
                bat '''
                    setlocal enabledelayedexpansion

                    set "PROD_DEPLOY_DIR=%PROD_ROOT%\\current"
                    set "PROD_VENV_DIR=%PROD_DEPLOY_DIR%\\.venv"
                    set "PROD_LOG_FILE=%PROD_ROOT%\\logs\\taskpilot-prod.log"
                    set "PROD_PORT=%PROD_PORT%"
                    set "DB_HOST=%DB_HOST%"
                    set "DB_PORT=%DB_PORT%"
                    set "DB_USER=%PROD_DB_USER%"
                    set "DB_PASSWORD=%PROD_DB_PASSWORD%"
                    set "DB_NAME=%DB_NAME%"

                    echo Preparing the PROD runtime environment...
                    if exist "%PROD_VENV_DIR%" (
                        rmdir /S /Q "%PROD_VENV_DIR%"
                    )

                    "%PYTHON_EXE%" -m venv "%PROD_VENV_DIR%"
                    if errorlevel 1 (
                        echo ERROR: Failed to create the PROD virtual environment.
                        exit /b 1
                    )

                    "%PROD_VENV_DIR%\\Scripts\\python.exe" -m pip install --upgrade pip setuptools wheel >nul 2>&1
                    if errorlevel 1 (
                        echo ERROR: Failed to upgrade pip in PROD environment.
                        exit /b 1
                    )

                    "%PROD_VENV_DIR%\\Scripts\\python.exe" -m pip install -r "%PROD_DEPLOY_DIR%\\requirements.txt" >nul 2>&1
                    if errorlevel 1 (
                        echo ERROR: Failed to install backend dependencies in PROD environment.
                        exit /b 1
                    )

                    echo Initializing the PROD database and demo user...
                    "%PROD_VENV_DIR%\\Scripts\\python.exe" "%PROD_DEPLOY_DIR%\\database.py"
                    if errorlevel 1 (
                        echo ERROR: PROD database initialization failed.
                        exit /b 1
                    )

                    echo Stopping any previous TaskPilot PROD process on port %PROD_PORT%...
                    for /f "tokens=1,2,3,4,5" %%a in ('netstat -ano ^| findstr :%PROD_PORT%') do (
                        if not "%%e"=="" (
                            taskkill /PID %%e /F >nul 2>&1
                        )
                    )

                    if exist "%PROD_LOG_FILE%" (
                        del /Q "%PROD_LOG_FILE%"
                    )

                    echo Updating PROD .env configuration...
                    (
                        echo FLASK_ENV=%PROD_ENV%
                        echo SECRET_KEY=%PROD_SECRET_KEY%
                        echo DB_HOST=%DB_HOST%
                        echo DB_PORT=%DB_PORT%
                        echo DB_USER=%DB_USER%
                        echo DB_PASSWORD=%DB_PASSWORD%
                        echo DB_NAME=%DB_NAME%
                        echo PORT=%PROD_PORT%
                        echo HOST=0.0.0.0
                    ) > "%PROD_DEPLOY_DIR%\\.env"

                    echo Starting TaskPilot in the PROD environment on port %PROD_PORT%...
                    start "TaskPilot-PROD" /B "%PROD_VENV_DIR%\\Scripts\\python.exe" "%PROD_DEPLOY_DIR%\\app.py" > "%PROD_LOG_FILE%" 2>&1

                    echo Waiting for PROD backend to start...
                    timeout /T 15 /NOBREAK

                    echo Calling the TaskPilot PROD health endpoint: http://127.0.0.1:%PROD_PORT%/health
                    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
                        "$ErrorActionPreference='Stop'; " ^
                        "$response = Invoke-WebRequest -Uri 'http://127.0.0.1:%PROD_PORT%/health' -UseBasicParsing -TimeoutSec 20; " ^
                        "if ($response.StatusCode -ne 200) { " ^
                            "throw 'PROD health check returned status code ' + $response.StatusCode " ^
                        "}; " ^
                        "$body = $response.Content; " ^
                        "Write-Host 'Response Body: ' $body; " ^
                        "if ($body -notmatch 'healthy') { " ^
                            "throw 'PROD health endpoint response does not contain healthy status' " ^
                        "}; " ^
                        "Write-Host 'PROD health check passed'"

                    if errorlevel 1 (
                        echo ERROR: PROD health check failed.
                        echo Showing PROD log output:
                        type "%PROD_LOG_FILE%"
                        exit /b 1
                    )

                    echo PROD deployment and health check passed successfully.
                '''
                }
            }
        }
    }

    post {

        success {
            echo '''
==================================================
       TASKPILOT CI BUILD SUCCESSFUL
==================================================
'''
            echo "Build Number: #${BUILD_NUMBER}"
            echo "Branch: ${params.BRANCH_NAME}"
            echo "Status: SUCCESS"
        }

        failure {
            echo '''
==================================================
         TASKPILOT CI BUILD FAILED
==================================================
'''
            echo "Build Number: #${BUILD_NUMBER}"
            echo "Branch: ${params.BRANCH_NAME}"
            echo "Status: FAILURE"
            echo "Review the failed stage above."
        }

        always {
            echo 'TaskPilot CI pipeline execution completed.'
        }
    }
}