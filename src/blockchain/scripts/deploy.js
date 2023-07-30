// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// You can also run a script with `npx hardhat run <script>`. If you do that, Hardhat
// will compile your contracts, add the Hardhat Runtime Environment's members to the
// global scope, and execute the script.
const hre = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
 
  console.log("Deploying contracts with the account:", deployer.address);
 
  // DevicesRegistry Contract
  const DevicesRegistry = await ethers.getContractFactory("DevicesRegistry");
  console.log("\nDeploying DevicesRegistry contract");
  const devicesRegistry = await DevicesRegistry.deploy();
 
  console.log("DevicesRegistry Contract")
  console.log("address:", devicesRegistry.address);
 
  // DeviceBinding Contract
  const DeviceBinding = await ethers.getContractFactory("DeviceBinding");
  console.log("\nDeploying DeviceBinding contract");
  const deviceBinding = await DeviceBinding.deploy(devicesRegistry.address);
 
  console.log("DeviceBinding Contract")
  console.log("address:", deviceBinding.address);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
