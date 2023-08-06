/* Copyright (c) 2010-2019. The SimGrid Team. All rights reserved.          */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#include "simgrid/plugins/load.h"
#include "src/include/surf/surf.hpp"
#include "src/kernel/activity/ExecImpl.hpp"
#include "src/plugins/vm/VirtualMachineImpl.hpp"
#include <simgrid/s4u.hpp>

SIMGRID_REGISTER_PLUGIN(host_load, "Cpu load", &sg_host_load_plugin_init)

/** @addtogroup plugin_load

This plugin makes it very simple for users to obtain the current load for each host.

*/

XBT_LOG_NEW_DEFAULT_SUBCATEGORY(surf_plugin_load, surf, "Logging specific to the HostLoad plugin");

namespace simgrid {
namespace plugin {

static const double activity_uninitialized_remaining_cost = -1;

class HostLoad {
public:
  static simgrid::xbt::Extension<simgrid::s4u::Host, HostLoad> EXTENSION_ID;

  explicit HostLoad(simgrid::s4u::Host* ptr)
      : host_(ptr)
      , last_updated_(surf_get_clock())
      , last_reset_(surf_get_clock())
      , current_speed_(host_->get_speed())
      , current_flops_(host_->pimpl_cpu->get_constraint()->get_usage())
      , theor_max_flops_(0)
  {
  }
  ~HostLoad() = default;
  HostLoad() = delete;
  explicit HostLoad(simgrid::s4u::Host& ptr) = delete;
  explicit HostLoad(simgrid::s4u::Host&& ptr) = delete;

  double get_current_load();
  /** Get the the average load since last reset(), as a ratio
   *
   * That's the ratio (amount of flops that were actually computed) / (amount of flops that could have been computed at full speed)
   */
  double get_average_load() { update(); return (theor_max_flops_ == 0) ? 0 : computed_flops_ / theor_max_flops_; };
  /** Amount of flops computed since last reset() */
  double get_computed_flops() { update(); return computed_flops_; }
  /** Return idle time since last reset() */
  double get_idle_time() { update(); return idle_time_; }
  /** Return idle time over the whole simulation */
  double get_total_idle_time() { update(); return total_idle_time_; }
  void update();
  void add_activity(simgrid::kernel::activity::ExecImplPtr activity);
  void reset();

private:
  simgrid::s4u::Host* host_ = nullptr;
  /* Stores all currently ongoing activities (computations) on this machine */
  std::map<simgrid::kernel::activity::ExecImplPtr, /* cost still remaining*/double> current_activities;
  double last_updated_      = 0;
  double last_reset_        = 0;
  /**
   * current_speed each core is running at; we need to store this as the speed
   * will already have changed once we get notified
   */
  double current_speed_     = 0;
  /**
   * How many flops are currently used by all the processes running on this
   * host?
   */
  double current_flops_     = 0;
  double computed_flops_    = 0;
  double idle_time_         = 0;
  double total_idle_time_   = 0; /* This gets never reset */
  double theor_max_flops_   = 0;
};

simgrid::xbt::Extension<simgrid::s4u::Host, HostLoad> HostLoad::EXTENSION_ID;

void HostLoad::add_activity(simgrid::kernel::activity::ExecImplPtr activity)
{
  current_activities.insert({activity, activity_uninitialized_remaining_cost});
}

void HostLoad::update()
{
  double now = surf_get_clock();

  // This loop updates the flops that the host executed for the ongoing computations
  auto iter = begin(current_activities);
  while (iter != end(current_activities)) {
    auto& activity                         = iter->first;  // Just an alias
    auto& remaining_cost_after_last_update = iter->second; // Just an alias
    auto& action                           = activity->surf_action_;
    auto current_iter                      = iter;
    ++iter;

    if (action != nullptr && action->get_finish_time() != now && activity->state_ == e_smx_state_t::SIMIX_RUNNING) {
      if (remaining_cost_after_last_update == activity_uninitialized_remaining_cost) {
        remaining_cost_after_last_update = action->get_cost();
      }
      double computed_flops_since_last_update = remaining_cost_after_last_update - /*remaining now*/activity->get_remaining();
      computed_flops_                        += computed_flops_since_last_update;
      remaining_cost_after_last_update        = activity->get_remaining();
    }
    else if (activity->state_ == e_smx_state_t::SIMIX_DONE) {
      computed_flops_ += remaining_cost_after_last_update;
      current_activities.erase(current_iter);
    }
  }

  /* Current flop per second computed by the cpu; current_flops = k * pstate_speed_in_flops, k @in {0, 1, ..., cores-1}
   * designates number of active cores; will be 0 if CPU is currently idle */
  current_flops_ = host_->pimpl_cpu->get_constraint()->get_usage();

  if (current_flops_ == 0) {
    idle_time_ += (now - last_updated_);
    total_idle_time_ += (now - last_updated_);
    XBT_DEBUG("[%s]: Currently idle -> Added %f seconds to idle time (totaling %fs)", host_->get_cname(), (now - last_updated_), idle_time_);
  }

  theor_max_flops_ += current_speed_ * host_->get_core_count() * (now - last_updated_);
  current_speed_ = host_->get_speed();
  last_updated_  = now;
}

/** @brief Get the current load as a ratio = achieved_flops / (core_current_speed * core_amount)
 *
 * You may also want to check simgrid::s4u::Host::get_load() that simply returns
 * the achieved flop rate (in flops per seconds), ie the load that a new action arriving on
 * that host would suffer.
 *
 * Please note that this function only returns an instantaneous load that may be deceiving
 * in some scenarios. For example, imagine that an activity terminates at time t, and that
 * another activity is created on the same host at the exact same timestamp. The load was
 * never 0 on the simulated machine since the time did not advance between the two events.
 * But still, if you call this function between the two events (in the simulator course), it
 * returns 0 although there is no time (in the simulated time) where this value is valid.
 */
double HostLoad::get_current_load()
{
  // We don't need to call update() here because it is called every time an action terminates or starts
  return current_flops_ / static_cast<double>(host_->get_speed() * host_->get_core_count());
}

/*
 * Resets the counters
 */
void HostLoad::reset()
{
  last_updated_    = surf_get_clock();
  last_reset_      = surf_get_clock();
  idle_time_       = 0;
  computed_flops_  = 0;
  theor_max_flops_ = 0;
  current_flops_   = host_->pimpl_cpu->get_constraint()->get_usage();
  current_speed_   = host_->get_speed();
}
} // namespace plugin
} // namespace simgrid

using simgrid::plugin::HostLoad;

/* **************************** events  callback *************************** */
/* This callback is fired either when the host changes its state (on/off) or its speed
 * (because the user changed the pstate, or because of external trace events) */
static void on_host_change(simgrid::s4u::Host const& host)
{
  if (dynamic_cast<simgrid::s4u::VirtualMachine const*>(&host)) // Ignore virtual machines
    return;

  host.extension<HostLoad>()->update();
}

/* **************************** Public interface *************************** */

/** @brief Initializes the HostLoad plugin
 * @details The HostLoad plugin provides an API to get the current load of each host.
 */
void sg_host_load_plugin_init()
{
  if (HostLoad::EXTENSION_ID.valid())
    return;

  HostLoad::EXTENSION_ID = simgrid::s4u::Host::extension_create<HostLoad>();

  if (simgrid::s4u::Engine::is_initialized()) { // If not yet initialized, this would create a new instance
                                                // which would cause seg faults...
    simgrid::s4u::Engine* e = simgrid::s4u::Engine::get_instance();
    for (auto& host : e->get_all_hosts()) {
      host->extension_set(new HostLoad(host));
    }
  }

  /* When attaching a callback into a signal, you can use a lambda as follows, or a regular function as done below */

  simgrid::s4u::Host::on_creation.connect([](simgrid::s4u::Host& host) {
    if (dynamic_cast<simgrid::s4u::VirtualMachine*>(&host)) // Ignore virtual machines
      return;
    host.extension_set(new HostLoad(&host));
  });

  simgrid::kernel::activity::ExecImpl::on_creation.connect([](simgrid::kernel::activity::ExecImpl& activity) {
    if (activity.get_host_number() == 1) { // We only run on one host
      simgrid::s4u::Host* host         = activity.get_host();
      simgrid::s4u::VirtualMachine* vm = dynamic_cast<simgrid::s4u::VirtualMachine*>(host);
      if (vm != nullptr)
        host = vm->get_pm();
      xbt_assert(host != nullptr);
      host->extension<HostLoad>()->add_activity(&activity);
      host->extension<HostLoad>()->update(); // If the system was idle until now, we need to update *before*
                                             // this computation starts running so we can keep track of the
                                             // idle time. (Communication operations don't trigger this hook!)
    }
    else { // This runs on multiple hosts
      XBT_DEBUG("HostLoad plugin currently does not support executions on several hosts");
    }
  });
  simgrid::kernel::activity::ExecImpl::on_completion.connect([](simgrid::kernel::activity::ExecImpl const& activity) {
    if (activity.get_host_number() == 1) { // We only run on one host
      simgrid::s4u::Host* host         = activity.get_host();
      simgrid::s4u::VirtualMachine* vm = dynamic_cast<simgrid::s4u::VirtualMachine*>(host);
      if (vm != nullptr)
        host = vm->get_pm();
      xbt_assert(host != nullptr);
      host->extension<HostLoad>()->update();
    }
    else { // This runs on multiple hosts
      XBT_DEBUG("HostLoad plugin currently does not support executions on several hosts");
    }
  });
  simgrid::s4u::Host::on_state_change.connect(&on_host_change);
  simgrid::s4u::Host::on_speed_change.connect(&on_host_change);
}

/** @brief Returns the current load of that host, as a ratio = achieved_flops / (core_current_speed * core_amount)
 *
 *  See simgrid::plugin::HostLoad::get_current_load() for the full documentation.
 */
double sg_host_get_current_load(sg_host_t host)
{
  xbt_assert(HostLoad::EXTENSION_ID.valid(),
             "The Load plugin is not active. Please call sg_host_load_plugin_init() during initialization.");

  return host->extension<HostLoad>()->get_current_load();
}

/** @brief Returns the current load of the host passed as argument
 *
 *  See also @ref plugin_load
 */
double sg_host_get_avg_load(sg_host_t host)
{
  xbt_assert(HostLoad::EXTENSION_ID.valid(),
             "The Load plugin is not active. Please call sg_host_load_plugin_init() during initialization.");

  return host->extension<HostLoad>()->get_average_load();
}

/** @brief Returns the time this host was idle since the last reset
 *
 *  See also @ref plugin_load
 */
double sg_host_get_idle_time(sg_host_t host)
{
  xbt_assert(HostLoad::EXTENSION_ID.valid(),
             "The Load plugin is not active. Please call sg_host_load_plugin_init() during initialization.");

  return host->extension<HostLoad>()->get_idle_time();
}

double sg_host_get_total_idle_time(sg_host_t host)
{
  xbt_assert(HostLoad::EXTENSION_ID.valid(),
             "The Load plugin is not active. Please call sg_host_load_plugin_init() during initialization.");

  return host->extension<HostLoad>()->get_total_idle_time();
}

double sg_host_get_computed_flops(sg_host_t host)
{
  xbt_assert(HostLoad::EXTENSION_ID.valid(),
             "The Load plugin is not active. Please call sg_host_load_plugin_init() during initialization.");

  return host->extension<HostLoad>()->get_computed_flops();
}

void sg_host_load_reset(sg_host_t host)
{
  xbt_assert(HostLoad::EXTENSION_ID.valid(),
             "The Load plugin is not active. Please call sg_host_load_plugin_init() during initialization.");

  host->extension<HostLoad>()->reset();
}
