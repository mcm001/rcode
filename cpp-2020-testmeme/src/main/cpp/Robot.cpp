/*----------------------------------------------------------------------------*/
/* Copyright (c) 2018-2020 FIRST. All Rights Reserved.                        */
/* Open Source Software - may be modified and shared by FRC teams. The code   */
/* must be accompanied by the FIRST BSD license file in the root directory of */
/* the project.                                                               */
/*----------------------------------------------------------------------------*/

#include "Robot.h"
#include "NumericalIntegration.h"
#include <iostream>
#include "frc/system/plant/DCMotor.h"
#include "units/length.h"
#include "units/mass.h"
#include "frc/system/plant/LinearSystemId.h"

void Robot::RobotInit() {
  static constexpr double kElevatorGearing = 100.0;
  static constexpr units::meter_t kElevatorDrumRadius = 0.5_in;
  static constexpr units::kilogram_t kCarriageMass = 4.0_kg;
  frc::DCMotor m_elevatorGearbox = frc::DCMotor::Vex775Pro(4);

  frc::LinearSystem<2, 1, 1> system = frc::LinearSystemId::ElevatorSystem(
      m_elevatorGearbox, kCarriageMass, kElevatorDrumRadius, kElevatorGearing);

  Eigen::Matrix<double, 2, 1> x0 = frc::MakeMatrix<2, 1>(0.0, 0.0);
  Eigen::Matrix<double, 1, 1> u0 = frc::MakeMatrix<1, 1>(12.0);

  Eigen::Matrix<double, 2, 1> x1 = frc::MakeMatrix<2, 1>(0.0, 0.0);
  for (size_t i = 0; i < 50; i++) {
    x1 = frc::RKF45(
        [&](Eigen::Matrix<double, 2, 1> x, Eigen::Matrix<double, 1, 1> u) {
          return system.A() * x + system.B() * u;
        },
        x1, u0, 0.020_s);
  }

  std::cout << "Estimated a distance of " << x1(0) << " while it should be " << system.CalculateX(x0, u0, 1_s)(0) << std::endl;
}
void Robot::RobotPeriodic() {}

void Robot::AutonomousInit() {}
void Robot::AutonomousPeriodic() {}

void Robot::TeleopInit() {}
void Robot::TeleopPeriodic() {}

void Robot::DisabledInit() {}
void Robot::DisabledPeriodic() {}

void Robot::TestInit() {}
void Robot::TestPeriodic() {}

#ifndef RUNNING_FRC_TESTS
int main() { return frc::StartRobot<Robot>(); }
#endif
