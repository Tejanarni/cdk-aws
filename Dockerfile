# Set the security protocol to TLS 1.2
ENV DOTNET_SYSTEM_NET_HTTP_USESOCKETSHTTPHANDLER=0
ENV DOTNET_SYSTEM_NET_HTTP_SOCKETSHTTPHANDLER_MAXREADBUFFERSIZE=2147483647
RUN echo "System.Net.ServicePointManager.SecurityProtocol = System.Net.SecurityProtocolType.Tls12;" > /usr/local/lib/SecurityProtocol.cs

# Compile the SecurityProtocol.cs file
RUN dotnet new console -n SecurityProtocol
COPY SecurityProtocol.cs /SecurityProtocol/SecurityProtocol.cs
RUN dotnet build -c Release /SecurityProtocol

# Use the compiled SecurityProtocol.dll in your application
ENTRYPOINT ["dotnet", "SecurityProtocol.dll"]





# Trust the development certificate
RUN dotnet dev-certs https -ep ${HOME}/.aspnet/https/aspnetapp.pfx -p <YOUR PASSWORD>

# Add the certificate to the local machine store
RUN dotnet dev-certs https --trust

# Copy the certificate to the container
COPY --from=build-env ${HOME}/.aspnet/https/aspnetapp.pfx /usr/local/share/aspnetapp.pfx

# Use the certificate in your application
ENV ASPNETCORE_URLS=https://+:443;http://+:80
ENV ASPNETCORE_HTTPS_PORT=443
ENV ASPNETCORE_Kestrel__Certificates__Default__Path=/usr/local/share/aspnetapp.pfx
ENV ASPNETCORE_Kestrel__Certificates__Default__Password=<YOUR PASSWORD>



