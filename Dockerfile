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



