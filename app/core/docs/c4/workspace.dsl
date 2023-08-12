/*
use the structurizr VScode extention
*/

workspace "Big Bank plc" "This is an example workspace to illustrate the key features of Structurizr, via the DSL, based around a fictional online banking system." {

    model {
        customer = person "Customer" "A customer of Kieback&Peter, with authority over installation(s)." "Customer"
        energy_provider = softwaresystem "Energy Provider" "Facilitates energy measurements (water, gas, electra) from a third party"

        enterprise "Kieback & Peter | NL" {
            sales_staff = person "Sales Staff" "Handles new customers" "Bank Staff" {
                properties {
                    "Location" "Customer Services"
                }
            }

            mainframe = softwaresystem "Mainframe KP" "Stores all of the core information about customers, accounts, transactions, etc."

            app_system = softwaresystem "Web Application" "Provides all functionality to customers via their web browser." "Web Browser"{
                webpage_container = container "Static Webpage" "Delivers the static content and the Internet banking single page application." "Java and Spring MVC"
                insight_container = container "Insights" "Gain instalaltioninsights"
                casting_container = container "Narrowcasting" "Narrowcasting"
                steering_container = container "Smart Steering" "Installation utilities"

            }
            back_office_app_system = softwaresystem "Employee Web Application" "Provides all functionality to employees via their web browser." "Web Browser"{
                back_office_insight_container = container "Employee Insights" "Overview of all installations and users"
                back_office_onboarding_container = container "Onboarding" "Assign user to installation or provide demo account"
            }

            web_balancer = softwaresystem "Webservices" "Network gateway and load balancer for services" {
                properties {
                    "Owner" "Customer Services"
                    "Development Team" "Dev/Internet Services"
                }
                energy_container = container "Energy" "Provides all of the Internet banking functionality to customers via their web browser." {
                    task_component = component "Task Component" "Schedules and send tasks"
                }
                endi_container = container "ENDI" "Provides all of the Internet banking functionality to customers via their web browser."
                api_container = container "API Gateway" "Provides webservices " "REST API" {
                    signinController = component "Sign In Controller" "Allows users to sign in to the Internet Banking System." "Spring MVC Rest Controller"
                    accountsSummaryController = component "Accounts Summary Controller" "Provides customers with a summary of their bank accounts." "Spring MVC Rest Controller"
                    resetPasswordController = component "Reset Password Controller" "Allows users to reset their passwords with a single use URL." "Spring MVC Rest Controller"
                    securityComponent = component "Security Component" "Provides functionality related to signing in, changing passwords, etc." "Spring Bean"
                    mainframeBankingSystemFacade = component "Mainframe Banking System Facade" "A facade onto the mainframe banking system." "Spring Bean"
                    service_component = component "Service Component" "Sends services to users." "Spring Bean"
                }
                worker_container = container "Worker" "Offload the work of itensive tasks"
                database = container "Database" "Stores user registration information, hashed authentication credentials, access logs, etc." "Oracle Database Schema" "Database"
            }            
        }


        # relationships between people and software systems
        customer -> app_system "Visits kieback-peter.net for webservices"
        customer -> sales_staff "Request demo"
        sales_staff -> back_office_onboarding_container "Create demo account"


        api_container -> energy_container "Add installation"
        task_component -> worker_container "Request data fetching"
        worker_container -> energy_provider "Fetch data"
        worker_container -> database "Write data"

        back_office_app_system -> web_balancer "Allow only from within VPN"
        app_system -> web_balancer "Make API requests"


        # relationships to/from containers
        # webpage_container -> energy_container "Request one of the services from web browser"
        signinController -> securityComponent "Uses"
        accountsSummaryController -> mainframeBankingSystemFacade "Uses"
        resetPasswordController -> securityComponent "Uses"
        resetPasswordController -> service_component "Uses"
        securityComponent -> database "Reads from and writes to" "JDBC"
        mainframeBankingSystemFacade -> mainframe "Makes API calls to" "XML/HTTPS"

        deploymentEnvironment "Development" {
            deploymentNode "Developer Laptop" "" "Microsoft Windows 10 or Apple macOS" {
                deploymentNode "Web Browser" "" "Chrome, Firefox, Safari, or Edge" {
                    developerenergy_containerInstance = containerInstance energy_container
                }
                deploymentNode "Docker Container - Web Server" "" "Docker" {
                    deploymentNode "Apache Tomcat" "" "Apache Tomcat 8.x" {
                        developerwebpage_containerInstance = containerInstance webpage_container
                        developerapi_containerInstance = containerInstance api_container
                    }
                }
                deploymentNode "Docker Container - Database Server" "" "Docker" {
                    deploymentNode "Database Server" "" "Oracle 12c" {
                        developerDatabaseInstance = containerInstance database
                    }
                }
            }
            deploymentNode "Big Bank plc" "" "Big Bank plc data center" "" {
                deploymentNode "bigbank-dev001" "" "" "" {
                    softwareSystemInstance mainframe
                }
            }

        }

        deploymentEnvironment "Live" {
            // deploymentNode "Customer's mobile device" "" "Apple iOS or Android" {
                // livemobile_containerInstance = containerInstance mobile_container
            // }
            deploymentNode "Customer's computer" "" "Microsoft Windows or Apple macOS" {
                deploymentNode "Web Browser" "" "Chrome, Firefox, Safari, or Edge" {
                    liveenergy_containerInstance = containerInstance energy_container
                }
            }

            deploymentNode "Big Bank plc" "" "Big Bank plc data center" {
                deploymentNode "bigbank-web***" "" "Ubuntu 16.04 LTS" "" 4 {
                    deploymentNode "Apache Tomcat" "" "Apache Tomcat 8.x" {
                        livewebpage_containerInstance = containerInstance webpage_container
                    }
                }
                deploymentNode "bigbank-api***" "" "Ubuntu 16.04 LTS" "" 8 {
                    deploymentNode "Apache Tomcat" "" "Apache Tomcat 8.x" {
                        liveapi_containerInstance = containerInstance api_container
                    }
                }

                deploymentNode "bigbank-db01" "" "Ubuntu 16.04 LTS" {
                    primaryDatabaseServer = deploymentNode "Oracle - Primary" "" "Oracle 12c" {
                        livePrimaryDatabaseInstance = containerInstance database
                    }
                }
                deploymentNode "bigbank-db02" "" "Ubuntu 16.04 LTS" "Failover" {
                    secondaryDatabaseServer = deploymentNode "Oracle - Secondary" "" "Oracle 12c" "Failover" {
                        liveSecondaryDatabaseInstance = containerInstance database "Failover"
                    }
                }
                deploymentNode "bigbank-prod001" "" "" "" {
                    softwareSystemInstance mainframe
                }
            }

            primaryDatabaseServer -> secondaryDatabaseServer "Replicates data to"
        }
    }

    views {
        properties {
            "c4plantuml.elementProperties" "true"
            "generatr.style.colors.primary" "#485fc7"
            "generatr.style.colors.secondary" "#ffffff"
            "generatr.style.faviconPath" "site/favicon.ico"
            "generatr.style.logoPath" "site/logo.png"

            // full list of available "generatr.markdown.flexmark.extensions"
            // "Abbreviation,Admonition,AnchorLink,Aside,Attributes,Autolink,Definition,Emoji,EnumeratedReference,Footnotes,GfmIssues,GfmStrikethroughSubscript,GfmTaskList,GfmUsers,GitLab,Ins,Macros,MediaTags,ResizableImage,Superscript,Tables,TableOfContents,SimulatedTableOfContents,Typographic,WikiLinks,XWikiMacro,YAMLFrontMatter,YouTubeLink"
            // see https://github.com/vsch/flexmark-java/wiki/Extensions
            // ATTENTION:
            // * "generatr.markdown.flexmark.extensions" values must be separated by comma
            // * it's not possible to use "GitLab" and "ResizableImage" extensions together
            // default behaviour, if no generatr.markdown.flexmark.extensions property is specified, is to load the Tables extension only
            "generatr.markdown.flexmark.extensions" "Abbreviation,Admonition,AnchorLink,Attributes,Autolink,Definition,Emoji,Footnotes,GfmTaskList,GitLab,MediaTags,Tables,TableOfContents,Typographic"
        }

        systemlandscape "SystemLandscape" {
            include *
            autoLayout
        }

        systemcontext web_balancer "WebSystem" {
            include *
            animation {
                web_balancer
                mainframe
            }
            autoLayout
        }
        # container app_system "AppContainers" {
        #     include *
        #     autoLayout

        # }

        container web_balancer "Containers" {
            include *
            animation {
                customer mainframe
                energy_container
                // mobile_container
                api_container
                database
            }
            autoLayout
        }

        component api_container "Components" {
            include *
            animation {
                database
                signinController securityComponent
                accountsSummaryController mainframeBankingSystemFacade
                resetPasswordController service_component
            }
            autoLayout
        }

        dynamic api_container "SignIn" "Summarises how the sign in feature works in the single-page application." {
            signinController -> securityComponent "Validates credentials using"
            securityComponent -> database "select * from users where username = ?"
            database -> securityComponent "Returns user data to"
            securityComponent -> signinController "Returns true if the hashed password matches"
            autoLayout
        }

        # deployment web_balancer "Development" "DevelopmentDeployment" {
        #     include *
        #     animation {
        #         developerenergy_containerInstance
        #         developerwebpage_containerInstance developerapi_containerInstance
        #         developerDatabaseInstance
        #     }
        #     autoLayout
        # }

        # deployment web_balancer "Live" "LiveDeployment" {
        #     include *
        #     animation {
        #         liveenergy_containerInstance
        #         // livemobile_containerInstance
        #         livewebpage_containerInstance liveapi_containerInstance
        #         livePrimaryDatabaseInstance
        #         liveSecondaryDatabaseInstance
        #     }
        #     autoLayout
        # }

        styles {
            element "Person" {
                color #ffffff
                fontSize 22
                shape Person
            }
            element "Customer" {
                background #08427b
            }
            element "Bank Staff" {
                background #999999
            }
            element "Software System" {
                background #1168bd
                color #ffffff
            }
            element "Existing System" {
                background #999999
                color #ffffff
            }
            element "Container" {
                background #438dd5
                color #ffffff
            }
            element "Web Browser" {
                shape WebBrowser
            }
            element "Mobile App" {
                shape MobileDeviceLandscape
            }
            element "Database" {
                shape Cylinder
            }
            element "Component" {
                background #85bbf0
                color #000000
            }
            element "Failover" {
                opacity 25
            }
        }
    }
}