// // // ═══════════════════════════════════════════════════════════════
// // // TaskPilot Jenkins CI/CD Pipeline
// // // ═══════════════════════════════════════════════════════════════
// // //
// // // Pipeline: Declarative
// // // Repository: TaskPilot (GitHub)
// // // Purpose: Automated CI pipeline for development builds
// // //
// // // Stages:
// // //   1. Checkout      - Clone repository from GitHub
// // //   2. Backend Setup - Install Python dependencies
// // //   3. Backend Tests - Run backend unit tests
// // //   4. Frontend Setup - Install Node.js dependencies
// // //   5. Frontend Build - Build React application
// // //   6. Success/Failure Status
// // //
// // // Environment Variables:
// // //   - PYTHON_VERSION: 3.13
// // //   - NODE_VERSION: 18+
// // //   - BUILD_TIMEOUT: 15 minutes
// // //
// // // ═══════════════════════════════════════════════════════════════

// // pipeline {
// //     agent any

// //     options {
// //         // ── Build Management ──
// //         buildDiscarder(
// //             logRotator(numToKeepStr: '10', artifactNumToKeepStr: '5')
// //         )
// //         timeout(time: 15, unit: 'MINUTES')
// //         timestamps()
        
// //         // ── Concurrent Builds ──
// //         disableConcurrentBuilds()
// //     }

// //     parameters {
// //         // ── Optional Parameters for Manual Runs ──
// //         string(
// //             name: 'BRANCH_NAME',
// //             defaultValue: 'main',
// //             description: 'Git branch to build'
// //         )
// //     }

// //     environment {
// //         // ── Project Paths ──
// //         BACKEND_DIR = '.'
// //         FRONTEND_DIR = 'frontend'
        
// //         // ── Build Identifiers ──
// //         BUILD_ID_SUFFIX = "${BUILD_TIMESTAMP}".replace(' ', '_').replace(':', '-')
        
// //         // ── Python Configuration ──
// //         VENV_DIR = "${WORKSPACE}/.venv"
// //         PYTHONPATH = "${WORKSPACE}"
        
// //         // ── Node Configuration ──
// //         NODE_PATH = "${FRONTEND_DIR}/node_modules"
// //     }

// //     stages {
// //         // ═══════════════════════════════════════════════════════════════
// //         // STAGE 1: CHECKOUT
// //         // ═══════════════════════════════════════════════════════════════
// //         stage('Checkout') {
// //             steps {
// //                 script {
// //                     echo "╔════════════════════════════════════════════════╗"
// //                     echo "║             STAGE: CHECKOUT                    ║"
// //                     echo "╚════════════════════════════════════════════════╝"
                    
// //                     try {
// //                         checkout([
// //                             $class: 'GitSCM',
// //                             branches: [[name: "*/${params.BRANCH_NAME}"]],
// //                             userRemoteConfigs: [[
// //                                 url: 'https://github.com/tanishqtiwari45/TaskPilot.git',
// //                                 credentialsId: 'github-credentials'
// //                             ]]
// //                         ])
                        
// //                         echo "✓ Repository cloned successfully"
// //                         echo "✓ Branch: ${params.BRANCH_NAME}"
// //                         echo "✓ Workspace: ${WORKSPACE}"
                        
// //                     } catch (Exception e) {
// //                         echo "✗ Checkout failed: ${e.message}"
// //                         throw e
// //                     }
// //                 }
// //             }
// //         }

// //         // ═══════════════════════════════════════════════════════════════
// //         // STAGE 2: BACKEND SETUP
// //         // ═══════════════════════════════════════════════════════════════
// //         stage('Backend Setup') {
// //             steps {
// //                 script {
// //                     echo "╔════════════════════════════════════════════════╗"
// //                     echo "║          STAGE: BACKEND SETUP                  ║"
// //                     echo "╚════════════════════════════════════════════════╝"
                    
// //                     try {
// //                         // Check Python version
// //                         echo "→ Checking Python version..."
// //                         sh '''
// //                             python --version
// //                             python -m pip --version
// //                         '''
                        
// //                         // Create virtual environment
// //                         echo "→ Creating Python virtual environment..."
// //                         sh '''
// //                             rm -rf ${VENV_DIR}
// //                             python -m venv ${VENV_DIR}
// //                         '''
                        
// //                         // Upgrade pip
// //                         echo "→ Upgrading pip..."
// //                         sh '''
// //                             . ${VENV_DIR}/bin/activate
// //                             pip install --upgrade pip setuptools wheel
// //                         '''
                        
// //                         // Install dependencies
// //                         echo "→ Installing backend dependencies..."
// //                         sh '''
// //                             . ${VENV_DIR}/bin/activate
// //                             pip install -r requirements.txt
// //                         '''
                        
// //                         // Verify installation
// //                         echo "→ Verifying installation..."
// //                         sh '''
// //                             . ${VENV_DIR}/bin/activate
// //                             pip list
// //                         '''
                        
// //                         echo "✓ Backend setup completed successfully"
                        
// //                     } catch (Exception e) {
// //                         echo "✗ Backend setup failed: ${e.message}"
// //                         throw e
// //                     }
// //                 }
// //             }
// //         }

// //         // ═══════════════════════════════════════════════════════════════
// //         // STAGE 3: BACKEND TESTS
// //         // ═══════════════════════════════════════════════════════════════
// //         stage('Backend Tests') {
// //             steps {
// //                 script {
// //                     echo "╔════════════════════════════════════════════════╗"
// //                     echo "║          STAGE: BACKEND TESTS                  ║"
// //                     echo "╚════════════════════════════════════════════════╝"
                    
// //                     try {
// //                         echo "→ Checking for test files..."
                        
// //                         // Run unit tests if they exist
// //                         sh '''
// //                             . ${VENV_DIR}/bin/activate
                            
// //                             # Check if tests directory exists
// //                             if [ -d "tests" ]; then
// //                                 echo "✓ Tests directory found"
// //                                 echo "→ Running pytest..."
// //                                 pip install pytest pytest-cov > /dev/null 2>&1
// //                                 pytest tests/ -v --tb=short
// //                             else
// //                                 echo "⚠ No tests directory found"
// //                                 echo "→ Running code syntax check..."
// //                                 python -m py_compile app.py config.py auth.py database.py models.py utils.py
// //                                 echo "✓ Code syntax check passed"
// //                             fi
// //                         '''
                        
// //                         echo "✓ Backend tests completed"
                        
// //                     } catch (Exception e) {
// //                         echo "⚠ Backend tests warning: ${e.message}"
// //                         // Don't fail the build for now since tests don't exist yet
// //                         echo "→ Continuing pipeline (tests not yet configured)"
// //                     }
// //                 }
// //             }
// //         }

// //         // ═══════════════════════════════════════════════════════════════
// //         // STAGE 4: FRONTEND SETUP
// //         // ═══════════════════════════════════════════════════════════════
// //         stage('Frontend Setup') {
// //             steps {
// //                 script {
// //                     echo "╔════════════════════════════════════════════════╗"
// //                     echo "║         STAGE: FRONTEND SETUP                  ║"
// //                     echo "╚════════════════════════════════════════════════╝"
                    
// //                     try {
// //                         // Check Node.js version
// //                         echo "→ Checking Node.js and npm versions..."
// //                         sh '''
// //                             node --version
// //                             npm --version
// //                         '''
                        
// //                         // Install dependencies
// //                         echo "→ Installing frontend dependencies..."
// //                         sh '''
// //                             cd ${FRONTEND_DIR}
// //                             npm ci --prefer-offline --no-audit
// //                         '''
                        
// //                         // Verify installation
// //                         echo "→ Verifying npm packages..."
// //                         sh '''
// //                             cd ${FRONTEND_DIR}
// //                             npm list | head -20
// //                             echo "..."
// //                         '''
                        
// //                         echo "✓ Frontend setup completed successfully"
                        
// //                     } catch (Exception e) {
// //                         echo "✗ Frontend setup failed: ${e.message}"
// //                         throw e
// //                     }
// //                 }
// //             }
// //         }

// //         // ═══════════════════════════════════════════════════════════════
// //         // STAGE 5: FRONTEND BUILD
// //         // ═══════════════════════════════════════════════════════════════
// //         stage('Frontend Build') {
// //             steps {
// //                 script {
// //                     echo "╔════════════════════════════════════════════════╗"
// //                     echo "║         STAGE: FRONTEND BUILD                  ║"
// //                     echo "╚════════════════════════════════════════════════╝"
                    
// //                     try {
// //                         echo "→ Building React application with Vite..."
// //                         sh '''
// //                             cd ${FRONTEND_DIR}
// //                             npm run build
// //                         '''
                        
// //                         // Verify build output
// //                         echo "→ Verifying build output..."
// //                         sh '''
// //                             if [ -d "${FRONTEND_DIR}/dist" ]; then
// //                                 echo "✓ Build directory found"
// //                                 echo "Build artifacts:"
// //                                 ls -lah ${FRONTEND_DIR}/dist/ | head -10
// //                                 echo "..."
// //                                 echo "Total files: $(find ${FRONTEND_DIR}/dist -type f | wc -l)"
// //                             else
// //                                 echo "✗ Build directory not found!"
// //                                 exit 1
// //                             fi
// //                         '''
                        
// //                         echo "✓ Frontend build completed successfully"
                        
// //                     } catch (Exception e) {
// //                         echo "✗ Frontend build failed: ${e.message}"
// //                         throw e
// //                     }
// //                 }
// //             }
// //         }

// //     }

// //     // ═══════════════════════════════════════════════════════════════════════
// //     // POST BUILD ACTIONS
// //     // ═══════════════════════════════════════════════════════════════════════
// //     post {
// //         always {
// //             script {
// //                 echo "╔════════════════════════════════════════════════╗"
// //                 echo "║          BUILD CLEANUP & SUMMARY               ║"
// //                 echo "╚════════════════════════════════════════════════╝"
                
// //                 // Archive build artifacts
// //                 sh '''
// //                     if [ -d "${FRONTEND_DIR}/dist" ]; then
// //                         echo "→ Archiving frontend build artifacts..."
// //                     fi
// //                 '''
                
// //                 // Clean up virtual environment (optional)
// //                 sh '''
// //                     echo "→ Build workspace size: $(du -sh ${WORKSPACE} | cut -f1)"
// //                 '''
// //             }
// //         }

// //         success {
// //             script {
// //                 echo "╔════════════════════════════════════════════════╗"
// //                 echo "║               ✓ BUILD SUCCESSFUL                ║"
// //                 echo "╚════════════════════════════════════════════════╝"
// //                 echo ""
// //                 echo "Build Details:"
// //                 echo "  • Build Number: #${BUILD_NUMBER}"
// //                 echo "  • Branch: ${params.BRANCH_NAME}"
// //                 echo "  • Duration: ${currentBuild.durationString}"
// //                 echo ""
// //                 echo "Next Steps:"
// //                 echo "  → UAT Deployment (manual trigger)"
// //                 echo "  → Docker Build (next phase)"
// //                 echo ""
// //             }
// //         }

// //         failure {
// //             script {
// //                 echo "╔════════════════════════════════════════════════╗"
// //                 echo "║               ✗ BUILD FAILED                   ║"
// //                 echo "╚════════════════════════════════════════════════╝"
// //                 echo ""
// //                 echo "Build Details:"
// //                 echo "  • Build Number: #${BUILD_NUMBER}"
// //                 echo "  • Branch: ${params.BRANCH_NAME}"
// //                 echo "  • Duration: ${currentBuild.durationString}"
// //                 echo ""
// //                 echo "Failed Stage: ${env.STAGE_NAME}"
// //                 echo ""
// //                 echo "Action Required:"
// //                 echo "  → Review console output for errors"
// //                 echo "  → Fix issues and commit to GitHub"
// //                 echo "  → Pipeline will auto-trigger on next push"
// //                 echo ""
// //             }
// //         }

// //         unstable {
// //             script {
// //                 echo "╔════════════════════════════════════════════════╗"
// //                 echo "║               ⚠ BUILD UNSTABLE                 ║"
// //                 echo "╚════════════════════════════════════════════════╝"
// //                 echo "Some tests may have failed. Review logs."
// //             }
// //         }

// //         cleanup {
// //             script {
// //                 echo "→ Cleaning up workspace..."
// //                 deleteDir()
// //             }
// //         }
// //     }
// // }

// pipeline {
//     agent any

//     options {
//         buildDiscarder(
//             logRotator(
//                 numToKeepStr: '10',
//                 artifactNumToKeepStr: '5'
//             )
//         )

//         timeout(time: 15, unit: 'MINUTES')
//         timestamps()
//         disableConcurrentBuilds()
//     }

//     parameters {
//         string(
//             name: 'BRANCH_NAME',
//             defaultValue: 'main',
//             description: 'Git branch to build'
//         )
//     }

//     environment {
//         FRONTEND_DIR = 'frontend'
//         VENV_DIR = "${WORKSPACE}\\.venv"
//         PYTHONPATH = "${WORKSPACE}"
//         PYTHON_EXE = 'C:\\Users\\Tanishq Tiwari\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
//     }

//     stages {

//         stage('Checkout') {
//             steps {
//                 echo 'Checking out TaskPilot source code...'

//                 checkout([
//                     $class: 'GitSCM',
//                     branches: [[
//                         name: "*/${params.BRANCH_NAME}"
//                     ]],
//                     userRemoteConfigs: [[
//                         url: 'https://github.com/tanishqtiwari45/TaskPilot.git'
//                     ]]
//                 ])

//                 echo '✓ Repository checkout completed'
//             }
//         }

//         stage('Backend Setup') {
//             steps {
//                 echo 'Setting up Python backend environment...'

//                 bat '''
//                     echo Using workspace: "%WORKSPACE%"
//                     echo Using Python executable: "%PYTHON_EXE%"

//                     if not exist "%VENV_DIR%" (
//                         echo Creating virtual environment...
//                         "%PYTHON_EXE%" -m venv "%VENV_DIR%"
//                     ) else (
//                         echo Virtual environment already exists.
//                     )

//                     if not exist "%VENV_DIR%\\Scripts\\python.exe" (
//                         echo ERROR: Virtual environment python executable was not created.
//                         exit /b 1
//                     )

//                     echo Upgrading pip...
//                     "%VENV_DIR%\\Scripts\\python.exe" -m pip install --upgrade pip setuptools wheel

//                     echo Installing backend dependencies...
//                     "%VENV_DIR%\\Scripts\\python.exe" -m pip install -r requirements.txt

//                     echo Installing pytest for CI validation...
//                     "%VENV_DIR%\\Scripts\\python.exe" -m pip install pytest pytest-cov

//                     echo Backend setup completed successfully.
//                 '''
//             }
//         }

//         stage('Backend Tests') {
//             steps {
//                 echo 'Running backend tests...'

//                 bat '''
//                     if exist "%WORKSPACE%\\tests" (
//                         echo Tests directory found.
//                         echo Running pytest...
//                         "%VENV_DIR%\\Scripts\\python.exe" -m pytest tests -v --tb=short
//                     ) else if exist "%WORKSPACE%\\test_*.py" (
//                         echo Root-level test module found.
//                         echo Running pytest...
//                         "%VENV_DIR%\\Scripts\\python.exe" -m pytest test_*.py -v --tb=short
//                     ) else (
//                         echo No pytest suite found.
//                         echo Running Python syntax validation...
//                         "%VENV_DIR%\\Scripts\\python.exe" -m compileall -q .
//                         echo Python syntax validation completed successfully.
//                     )
//                 '''
//             }
//         }

//         stage('Frontend Setup') {
//             steps {
//                 echo 'Setting up React frontend...'

//                 bat '''
//                     cd /d "%WORKSPACE%\\frontend"

//                     if not exist "package.json" (
//                         echo ERROR: frontend/package.json was not found in the workspace.
//                         exit /b 1
//                     )

//                     node --version
//                     npm --version

//                     echo Installing frontend dependencies...
//                     if exist "package-lock.json" (
//                         npm ci --no-audit --no-fund
//                     ) else (
//                         npm install --no-audit --no-fund
//                     )

//                     echo Verifying Vite installation...
//                     npm ls vite --depth=0
//                     if not exist "node_modules\\vite\\bin\\vite.js" (
//                         echo ERROR: Vite dependency was not installed correctly.
//                         dir node_modules
//                         exit /b 1
//                     )

//                     echo Frontend setup completed successfully.
//                 '''
//             }
//         }

//         stage('Frontend Build') {
//             steps {
//                 echo 'Building React application...'

//                 bat '''
//                     cd /d "%WORKSPACE%\\frontend"
//                     npm run build

//                     if not exist "dist" (
//                         echo ERROR: Frontend dist directory was not created.
//                         exit /b 1
//                     )

//                     echo Frontend build completed successfully.
//                     echo Build output:
//                     dir dist
//                 '''
//             }
//         }
//     }

//     post {

//         success {
//             echo '''
// ==================================================
//         TASKPILOT CI BUILD SUCCESSFUL
// ==================================================
// '''
//             echo "Build Number: #${BUILD_NUMBER}"
//             echo "Branch: ${params.BRANCH_NAME}"
//         }

//         failure {
//             echo '''
// ==================================================
//         TASKPILOT CI BUILD FAILED
// ==================================================
// '''
//             echo "Build Number: #${BUILD_NUMBER}"
//             echo "Branch: ${params.BRANCH_NAME}"
//             echo "Check the Console Output for the failed stage."
//         }

//         always {
//             echo 'TaskPilot CI pipeline execution completed.'
//         }
//     }
// }



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

    environment {
        // Project
        FRONTEND_DIR = 'frontend'

        // Python
        PYTHON_EXE = 'C:\\Users\\Tanishq Tiwari\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
        VENV_DIR = "${WORKSPACE}\\.venv"
        PYTHONPATH = "${WORKSPACE}"
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
        // 2. BACKEND SETUP
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
                    node --version

                    if errorlevel 1 (
                        echo ERROR: Node.js is not available to Jenkins.
                        exit /b 1
                    )

                    echo.
                    echo npm version:
                    npm --version

                    if errorlevel 1 (
                        echo ERROR: npm is not available to Jenkins.
                        exit /b 1
                    )

                    echo.
                    echo Checking npm configuration...

                    npm config get registry

                    echo.
                    echo Removing old node_modules...

                    if exist "node_modules" (
                        rmdir /S /Q "node_modules"
                    )

                    echo.
                    echo Installing frontend dependencies...

                    if exist "package-lock.json" (

                        echo package-lock.json found.
                        echo Running npm ci...

                        npm ci --no-audit --no-fund

                        if errorlevel 1 (
                            echo ERROR: npm ci failed.
                            exit /b 1
                        )

                    ) else (

                        echo package-lock.json not found.
                        echo Running npm install...

                        npm install --no-audit --no-fund

                        if errorlevel 1 (
                            echo ERROR: npm install failed.
                            exit /b 1
                        )
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

                    npm ls vite --depth=0

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

                    npx --no-install vite --version

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

                    echo Running frontend production build...

                    // npx --no-install vite build
                       npm run build
                       
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

                    echo.
                    echo Frontend build completed successfully.

                    echo.
                    echo Build output:
                    dir "dist"
                '''
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